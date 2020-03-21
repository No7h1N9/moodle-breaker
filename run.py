import requests
import bs4
from urllib.parse import urlparse, parse_qs
from settings import LOGIN, PASSWORD, HOMEWORK_URLS, MEAN_URLS, MEAN_ATTEMPTS
import logging
from tasks_parser import parse_task_fields, parse_answers
import re


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return -1


def setup_logger(loglevel):
    logger = logging.getLogger("main")
    logger.setLevel(loglevel)
    # create the logging file handler
    fh = logging.FileHandler("main.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = setup_logger(logging.DEBUG)


class TaskMetadata:

    def __init__(self, session, task_url):
        self.task_url = task_url
        self.session = session
        self._task_metadata = None

    # Should be cached
    @property
    def task_metadata(self):
        if not self._task_metadata:
            # First run
            soup = bs4.BeautifulSoup(self.session.get(self.task_url).content, features='lxml')
            for tag in soup.find_all('input'):
                if tag.get('name', '') == 'cmid':
                    cmid = tag['value']
                if tag.get('name', '') == 'sesskey':
                    sess_key = tag['value']
            self._task_metadata = {'cmid': cmid, 'sesskey': sess_key}
        return self._task_metadata

    @property
    def cmid(self):
        return self.task_metadata['cmid']

    @property
    def sesskey(self):
        return self.task_metadata['sesskey']


class LoginManager:

    def __init__(self, login: str, password: str):
        self.login, self.password = login, password
        self._session, self._login_token = None, None

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session

    @property
    def login_token(self):
        if not self._login_token:
            soup = bs4.BeautifulSoup(self.session.get('http://moodle.phystech.edu/my/').content, features='lxml')
            self._login_token = soup.find('input', {'name': 'logintoken'})['value']
        return self._login_token

    def authorize(self):
        # 2. Авторизация
        response = self.session.post(
            'http://moodle.phystech.edu/login/index.php',
            {'username': self.login, 'password': self.password, 'anchor': '', 'logintoken': self.login_token}
        )
        return response

    @property
    def is_authorized(self):
        # 1. Проверка авторизации
        response = self.session.get('http://moodle.phystech.edu/my/')
        parsed = bs4.BeautifulSoup(response.content, features='lxml')
        return 'Вход' not in str(parsed.title)

    def __enter__(self):
        if not self.is_authorized:
            self.authorize()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Task:

    def __init__(self, task_url, session):
        self.task_url = task_url
        self.session = session
        self.task_metadata = TaskMetadata(session=session, task_url=task_url)
        self.task_fields = None
        self._task_data = None
        self.best_own_url = self.find_best_own_url()
        self.answer_dict = {}
        if self.best_own_url:
            logger.info('found own attempt: {}'.format(self.best_own_url))

    def find_best_own_url(self):
        response = self.session.get(
            'http://moodle.phystech.edu/mod/quiz/view.php?id={}'.format(self.task_metadata.cmid)
        )
        soup = bs4.BeautifulSoup(response.content, features='lxml')
        all_attempts = soup.find_all('tr')[1:]  # Первый - это хидер таблицы

        best_attempt = None
        try:
            # Надо определить, где находится твоя оценка
            total_cols = all_attempts[0].find_all('td', {'class', 'lastcol'})[0]['class']
            ide = [item for i, item in enumerate(total_cols) if re.search(r'c\d', item)]
            if ide:
                total_cols = int(ide[0][1:])

            all_attempts.sort(key=lambda tag: to_float(
                # В 'c3' содержится твоя оценка
                tag.find('td', {'class': f'c{total_cols - 1}'}).text.replace(',', '.')
            ))
            best_attempt = all_attempts.pop()
        except IndexError:
            logger.info('could not parse best own attempt. Proceeding as the first run...')
        best_url = None
        if best_attempt:
            best_url = best_attempt.find('td', {'class': f'c{total_cols}'}).next['href']
        return best_url

    def break_it(self):
        if not self.best_own_url:
            # Здесь мы чисто берем task_fields
            self.task_fields, _ = self.parse_task_fields(
                self.start_new_attempt()
            )
            self.upload_answers(attempt_number=_)
            self.finish_attempt(attempt_number=_)
            # Теперь ссылается на единственную попытку - свою
            self.best_own_url = self.find_best_own_url()
        self.task_fields, attempt = self.parse_task_fields(self.start_new_attempt())
        self.get_answers(self.best_own_url)
        self.upload_answers(attempt_number=attempt)
        self.finish_attempt(attempt_number=attempt)

    def start_new_attempt(self):
        response = self.session.post(
            'http://moodle.phystech.edu/mod/quiz/startattempt.php',
            {'cmid': self.task_metadata.cmid, 'sesskey': self.task_metadata.sesskey}
        )
        return response

    @staticmethod
    def parse_task_fields(response):
        task_fields = parse_task_fields(response)
        logger.debug(f'task_fields: {task_fields}')
        task_url = response.url
        logger.debug(f'task_url: {task_url}')
        attempt_number = parse_qs(urlparse(task_url).query)['attempt'][0]
        logger.debug(f'attempt_number: {attempt_number}')
        return task_fields, attempt_number

    def upload_answers(self, attempt_number):
        data = {'sesskey': self.task_metadata.sesskey,
                'attempt': attempt_number,
                # Параметры с мудла, без них не работает
                'nextpage': -1,
                'next': 'Закончить попытку...', 'scrollpos': '', 'thispage': 0, 'timeup': 0, 'slots': 1}
        for elem in self.task_fields:
            # HACK: some strange field
            data.update({'{}:1_:flagged'.format(elem.split(':')[0]): 0})
            data.update({'{}:1_:sequencecheck'.format(elem.split(':')[0]): 1})
            break
        if len(self.answer_dict) == 0:
            # Пустые ответы
            logger.info('Empty answers dict, sending empty data')
            for key in self.task_fields:
                data.update({key: ''})
        else:
            for key in self.task_fields:
                # Ищем подходящий ответ. Коварный мудл меняет ключи, но я тоже не дурак!
                # Короче, тут проблема такая: было "q50228:блабла1" - а становится "q50229:блабла1"
                # Ключевой момент: блабла1 остается тем же, на этом и сыграем!
                correct_key = None
                for key1 in self.answer_dict.keys():
                    if key1.split(':')[1] == key.split(':')[1]:
                        logger.debug(f'mapping keys: {key1} -> {key}')
                        correct_key = key1
                        break
                data.update({key: self.answer_dict[correct_key]})

        response = self.session.post(
            'http://moodle.phystech.edu/mod/quiz/processattempt.php?cmid={}'.format(self.task_metadata.cmid),
            data
        )
        return response

    def finish_attempt(self, attempt_number):
        response = self.session.post(
            'http://moodle.phystech.edu/mod/quiz/processattempt.php',
            {'attempt': attempt_number, 'finishattempt': 1,
             'cmid': self.task_metadata.cmid, 'sesskey': self.task_metadata.sesskey}
        )
        return response

    def get_answers(self, attempt_url):
        response = self.session.get(attempt_url)
        correct_answers = parse_answers(response, self.task_fields)
        self.answer_dict = correct_answers
        return correct_answers


def cheat_on(url, multiple=1):
    with LoginManager(login=LOGIN, password=PASSWORD) as session:
        task = Task(task_url=url, session=session)
        logger.info(f'starting task {task.task_url}')
        for _ in range(multiple):
            try:
                task.break_it()
            except Exception as e:
                logger.debug(f'cookies: {session.cookies}')
                logger.error(e, stack_info=True)
                raise e


if __name__ == '__main__':
    for url in HOMEWORK_URLS:
        cheat_on(url)
    for url in MEAN_URLS:
        cheat_on(url, multiple=MEAN_ATTEMPTS)
