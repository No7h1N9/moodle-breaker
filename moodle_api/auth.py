import bs4
import requests


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