import pytest
from unittest.mock import Mock
import os
import re
import json
from pathlib import Path
from moodle_api.auth import LoginManager
from moodle_api.problem import TaskMetadata, Task


basedir = Path(__file__).parent


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


@pytest.fixture(params=Path(basedir/'fixtures'/'attempt_page').iterdir(), scope='session')
def attempt_page_with_params(request):
    with open(request.param / 'index.htm') as page:
        with open(request.param / 'params.json') as params:
            yield page.read(), json.loads(params.read())


@pytest.fixture(scope='session')
def mock_session(attempt_page_with_params):
    mock = Mock()
    mock.get().content = attempt_page_with_params[0]
    yield mock


@pytest.fixture()
def task_obj(mock_session, attempt_page_with_params):
    _, params = attempt_page_with_params
    yield Task(params['url'], mock_session), params


@pytest.fixture(scope='session')
def task_metadata_fixture(attempt_page_with_params):
    mock = Mock()
    content, expected = attempt_page_with_params
    mock.get().content = content
    yield TaskMetadata(
        mock, f'http://moodle.phystech.edu/mod/quiz/view.php?id={expected["cmid"]}'
    ), expected
