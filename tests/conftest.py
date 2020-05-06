import pytest
import json
from itertools import chain
from typing import Tuple, Any
from pathlib import Path
from moodle_api.parsers import TaskMetadata
from moodle_api.pages import SummaryPage, FinishedAttemptPage, RunningAttemptPage

basedir = Path(__file__).parent


def load_fixture(directory) -> Tuple[str, Any]:
    with open(directory / 'index.htm') as page:
        with open(directory / 'params.json') as params:
            return page.read(), json.loads(params.read())


@pytest.fixture(params=Path(basedir/'fixtures'/'attempt_page').iterdir(), scope='session')
def summary_page(request) -> Tuple[bytes, dict]:
    yield load_fixture(request.param)


@pytest.fixture(scope='session')
def summary_parser(summary_page):
    content, params = summary_page
    yield SummaryPage(content), params


@pytest.fixture(params=Path(basedir/'fixtures'/'finished_task_page').iterdir(), scope='session')
def finished_attempt(request) -> Tuple[bytes, dict]:
    yield load_fixture(request.param)


@pytest.fixture(params=Path(basedir/'fixtures'/'running_task_page').iterdir(), scope='session')
def running_attempt(request) -> Tuple[bytes, dict]:
    yield load_fixture(request.param)


@pytest.fixture(scope='session')
def running_attempt_parser(running_attempt):
    content, expected = running_attempt
    yield RunningAttemptPage(content), expected


@pytest.fixture(scope='session')
def finished_attempt_parser(finished_attempt):
    content, params = finished_attempt
    yield FinishedAttemptPage(content), params


@pytest.fixture(scope='session',
                params=chain(
                    Path(basedir / 'fixtures' / 'attempt_page').iterdir(),
                    Path(basedir / 'fixtures' / 'finished_task_page').iterdir(),
                    Path(basedir / 'fixtures' / 'running_task_page').iterdir(),
                ))
def all_pages(request):
    yield load_fixture(request.param)


@pytest.fixture()
def task_metadata_from_all(all_pages):
    content, expected = all_pages
    yield TaskMetadata(content), expected
