import pytest
from unittest.mock import Mock
import os
import re
import json
from pathlib import Path
from moodle_api.auth import LoginManager
from moodle_api.problem import TaskMetadata


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


@pytest.fixture(params=Path('./fixtures/attempt_page/').iterdir())
def task_metadata_fixture(request):
    with open(request.param / 'index.htm') as page:
        with open(request.param / 'params.json') as params:
            mock = Mock()
            contents = page.read()
            mock.get().content = contents
            expected = json.loads(params.read())
            yield TaskMetadata(
                mock, 'http://moodle.phystech.edu/mod/quiz/view.php?id=43122'
            ), expected
