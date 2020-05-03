import pytest
from unittest.mock import Mock
import os
import re
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


@pytest.fixture(params=basedir.rglob('attempt_page.htm'))
def task_metadata_fixture(request):
    with open(request.param) as f:
        mock = Mock()
        contents = f.read()
        mock.get().content = contents
        real_cmid = re.findall(r'cmid=\d+', contents)[0][len('cmid='):]
        real_sesskey = re.findall(r'sesskey=\w+', contents)[0][len('sesskey='):]
        yield TaskMetadata(
            mock, 'http://moodle.phystech.edu/mod/quiz/view.php?id=43122'
        ), real_cmid, real_sesskey
