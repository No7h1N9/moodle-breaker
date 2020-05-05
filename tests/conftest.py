import pytest
from unittest.mock import Mock
import json
from typing import Tuple, Any
from pathlib import Path
from moodle_api.parsers import TaskMetadata
from moodle_api.pages import SummaryPage, FinishedAttemptPage

basedir = Path(__file__).parent


def load_fixture(directory) -> Tuple[str, Any]:
    with open(directory / 'index.htm') as page:
        with open(directory / 'params.json') as params:
            return page.read(), json.loads(params.read())


@pytest.fixture(params=Path(basedir/'fixtures'/'attempt_page').iterdir(), scope='session')
def attempt_page_with_params(request) -> Tuple[bytes, dict]:
    yield load_fixture(request.param)


@pytest.fixture(scope='session')
def mock_session(attempt_page_with_params):
    mock = Mock()
    mock.get().content = attempt_page_with_params[0]
    yield mock


@pytest.fixture(scope='session')
def summary_parser(attempt_page_with_params):
    content, params = attempt_page_with_params
    yield SummaryPage(content), params


@pytest.fixture(params=Path(basedir/'fixtures'/'task_page').iterdir(), scope='session')
def finished_attempt(request) -> Tuple[bytes, dict]:
    yield load_fixture(request.param)


@pytest.fixture(scope='session')
def finished_attempt_parser(finished_attempt):
    content, params = finished_attempt
    yield FinishedAttemptPage(content), params


@pytest.fixture(scope='session')
def task_metadata(attempt_page_with_params):
    content, expected = attempt_page_with_params
    yield TaskMetadata(content), expected
