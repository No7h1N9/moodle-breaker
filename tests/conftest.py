import pytest
import os
from moodle_api.auth import LoginManager


@pytest.fixture()
def login_manager():
    lm = LoginManager(
        login=os.environ.get('MOODLE_LOGIN'),
        password=os.environ.get('MOODLE_PASSWORD'))
    yield lm


@pytest.fixture()
def authed_login_manager(login_manager: LoginManager):
    login_manager.authorize()
    yield login_manager
