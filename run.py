import requests
import bs4
from urllib.parse import urlparse, parse_qs
from settings import LOGIN, PASSWORD, HOMEWORK_URLS, MEAN_URLS
import logging


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
            soup = bs4.BeautifulSoup(self.session.get('http://moodle.phystech.edu/my/').content)
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
        parsed = bs4.BeautifulSoup(response.content)
        return 'Вход' not in str(parsed.title)

    def __enter__(self):
        if not self.is_authorized:
            self.authorize()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Task:

    def __init__(self, task_url, session, loglevel=logging.INFO):
        self.task_url = task_url
        self.session = session
        self.logger = self.setup_logger(loglevel)
        self._task_metadata, self._logger = None, None
        self._task_data = None
        self.answer_dict = {}

    @staticmethod
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

    # NOTE: надо сбрасывать, чтобы начать новую попытку!
    @property
    def task_data(self):
        if not self._task_data:
            # 4. Стартуем задание
            # Note: `task_id` === `cmid`
            response = self.session.post(
                'http://moodle.phystech.edu/mod/quiz/startattempt.php',
                {'cmid': self.cmid, 'sesskey': self.sesskey}
            )
            # TODO: может быть другой тип задания
            # Сначала считаем, что
            task_fields = set([x.get('name')
                           for x in bs4.BeautifulSoup(response.content).find_all('input', {'class': 'form-control'})])
            if None in task_fields:
                task_fields.remove(None)
            self.logger.debug(f'task_fields: {task_fields}')
            task_url = response.url
            self.logger.debug(f'task_url: {task_url}')
            attempt_number = parse_qs(urlparse(task_url).query)['attempt'][0]
            self.logger.debug(f'attempt_number: {attempt_number}')
            self._task_data = {
                'fields': task_fields,
                # NOTE: пока не используется
                'url': task_url,
                'attempt_number': attempt_number
            }
        return self._task_data

    def start_new_attempt(self):
        self._task_data = None
        return self.task_data

    @property
    def task_fields(self):
        return self.task_data['fields']

    @property
    def attempt_number(self):
        return self.task_data['attempt_number']

    @property
    def cmid(self):
        return self.task_metadata['cmid']

    @property
    def sesskey(self):
        return self.task_metadata['sesskey']

    # Should be cached
    @property
    def task_metadata(self):
        if not self._task_metadata:
            # First run
            soup = bs4.BeautifulSoup(self.session.get(self.task_url).content)
            cmid = soup.find('div', {'class': 'quizstartbuttondiv'}).input.find('input', {'name': 'cmid'})['value']
            sess_key = soup.find('input', {'name': 'sesskey'})['value']
            soup.find_all('input', {'class': 'form-control'})
            self._task_metadata = {'cmid': cmid, 'sesskey': sess_key}
        return self._task_metadata

    def upload_answers(self):
        data = {'sesskey': self.sesskey,
                'attempt': self.attempt_number,
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
            self.logger.info('Empty answers dict, sending empty data')
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
                        self.logger.debug(f'mapping keys: {key1} -> {key}')
                        correct_key = key1
                        break
                data.update({key: self.answer_dict[correct_key]})

        response = self.session.post(
            'http://moodle.phystech.edu/mod/quiz/processattempt.php?cmid={}'.format(self.cmid),
            data
        )
        return response

    def finish_attempt(self):
        response = self.session.post(
            'http://moodle.phystech.edu/mod/quiz/processattempt.php',
            {'attempt': self.attempt_number, 'finishattempt': 1,
             'cmid': self.cmid, 'sesskey': self.sesskey}
        )
        return response

    def get_answers(self):
        response = self.session.get(
            'http://moodle.phystech.edu/mod/quiz/review.php?attempt={}&cmid={}'
                .format(self.attempt_number, self.cmid)
        )
        soup = bs4.BeautifulSoup(response.content)
        correct_answers = {}
        for field in self.task_fields:
            tag = soup.find_all('input', {'name': field})
            for i in tag[0].parent.find_all('span', {'class': 'feedbackspan'})[0].contents:
                if 'ильный' in i:
                    correct_ans = i.split(': ')[1]
                    correct_answers.update({field: correct_ans})
        self.answer_dict = correct_answers
        return correct_answers


def cheat_on(url):
    with LoginManager(login=LOGIN, password=PASSWORD) as session:
        task = Task(task_url=url, session=session, loglevel=logging.DEBUG)
        task.logger.info(f'starting task {task.task_url}')
        task.start_new_attempt()
        task.upload_answers()
        task.finish_attempt()
        task.get_answers()
        task.start_new_attempt()
        task.upload_answers()
        task.finish_attempt()


if __name__ == '__main__':
    for url in HOMEWORK_URLS:
        cheat_on(url)
    for url in MEAN_URLS:
        for _ in range(40):
            cheat_on(url)
