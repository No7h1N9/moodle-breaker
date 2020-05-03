import pytest
from unittest.mock import Mock
import os
from pathlib import Path
from moodle_api.auth import LoginManager
from moodle_api.problem import TaskMetadata


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


@pytest.fixture()
def task_metadata_fixture():
    with open(Path(__file__).parent/'fixtures'/'onepage_3_tasks'/'attempt_page.htm') as f:
        mock = Mock()
        mock.get().content = f.read()
        yield TaskMetadata(
            mock, 'http://moodle.phystech.edu/mod/quiz/view.php?id=43122')
