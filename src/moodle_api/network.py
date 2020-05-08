import requests
import bs4
from contextlib import contextmanager
from typing import Tuple
import re


class MoodleAPI:
    def __init__(self, login: str, password: str):
        self.login, self.password = login, password
        self._session = requests.Session()
        self._login_token = self._get_login_token()

    def auth(self):
        self._session.post(
            'http://moodle.phystech.edu/login/index.php',
            {'username': self.login, 'password': self.password,
             'anchor': '', 'logintoken': self._login_token})

    def _get_login_token(self) -> str:
        soup = bs4.BeautifulSoup(
            self._session.get('http://moodle.phystech.edu/my/').content,
            features='lxml')
        self._login_token = soup.find('input', {'name': 'logintoken'})['value']
        return self._login_token

    @property
    def is_authorized(self) -> bool:
        response = self._session.get('http://moodle.phystech.edu/my/')
        parsed = bs4.BeautifulSoup(response.content, features='lxml')
        return 'Вход' not in str(parsed.title)

    @contextmanager
    def session(self) -> requests.Session:
        if not self.is_authorized:
            self.auth()
        yield self._session

    def get_summary_page(self, cmid: str) -> requests.Response:
        with self.session() as s:
            return s.get(f'http://moodle.phystech.edu/mod/quiz/view.php?id={cmid}')

    def get_finished_attempt_page(self, cmid: str, attempt_id: str) -> Tuple[str, str]:
        with self.session() as s:
            return s.get(f'http://moodle.phystech.edu/mod/quiz/review.php?attempt={attempt_id}&cmid={cmid}')

    def start_attempt(self, cmid: str, sesskey: str) -> requests.Response:
        with self.session() as s:
            response = s.post(
                'http://moodle.phystech.edu/mod/quiz/startattempt.php',
                {'cmid': cmid, 'sesskey': sesskey}
            )
            if response.status_code == 404:
                raise ValueError('Cannot start attempt. Does task have limits?')
            return response

    def upload_answers(self, cmid: str, sesskey: str, attempt_id: str,
                       prefix: str, answers: dict) -> None:
        """

        :param sesskey:
        :param attempt_id:
        :param prefix: 'q643199'
        :param answers: {'1_sub6_answer': 'Hell', ...}
        """
        with self.session() as s:
            data = {'sesskey': sesskey,
                    'attempt': attempt_id,
                    # Параметры с мудла, без них не работает
                    'nextpage': -1,
                    'next': 'Закончить попытку...', 'scrollpos': '', 'thispage': 0, 'timeup': 0, 'slots': 1}
            # HACK: без этих странных полем мудл не съедает ответы
            slots = set([x.split('_')[0] for x in answers.keys()])
            for number in slots:
                data.update({'{}:{}_:flagged'.format(prefix, number): 0})
                data.update({'{}:{}_:sequencecheck'.format(prefix, number): 1})
            '''
            for key in answers.keys():
                # TODO: Перенести это в парсер
                # Ищем подходящий ответ. Коварный мудл меняет ключи, но я тоже не дурак!
                # Короче, тут проблема такая: было "q50228:блабла1" - а становится "q50229:блабла1"
                # Ключевой момент: блабла1 остается тем же, на этом и сыграем!
                correct_key = None
                for key1 in self.answer_dict.keys():
                    if key1.split(':')[1] == key.split(':')[1]:
                        logger.debug(f'mapping keys: {key1} -> {key}')
                        correct_key = key1
                        break
            '''
            for form, ans in answers.items():
                data.update({f'{prefix}:{form}': ans})

            response = s.post(
                'http://moodle.phystech.edu/mod/quiz/processattempt.php?cmid={}'.format(cmid),
                data
            )

    def finish_attempt(self, cmid: str, sesskey: str, attempt_id: str) -> None:
        with self.session() as s:
            s.post(
                'http://moodle.phystech.edu/mod/quiz/processattempt.php',
                {'attempt': attempt_id, 'finishattempt': 1,
                 'cmid': cmid, 'sesskey': sesskey}
            )

