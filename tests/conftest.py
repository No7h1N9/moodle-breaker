import pytest
from pathlib import Path
from pytest_cases import fixture

basedir = Path(__file__).parent

FIXTURE_PATH = Path(basedir/'fixtures')
ALL_COURSES_PAGE_DIR = FIXTURE_PATH/'all_courses_page'
ATTEMPT_PAGE_DIR = FIXTURE_PATH/'attempt_page'
RUNNING_ATTEMPT_DIR = FIXTURE_PATH/'running_task_page'
SINGLE_TYPE_DIR = FIXTURE_PATH/'finished_task_page'/'single_type'

PICKER_ONLY_DIR = SINGLE_TYPE_DIR/'picker'
INPUT_ONLY_DIR = SINGLE_TYPE_DIR/'input'
RADIO_ONLY_DIR = SINGLE_TYPE_DIR/'radio'
CHECKBOX_ONLY_DIR = SINGLE_TYPE_DIR/'checkbox'


@fixture
@pytest.mark.parametrize('directory', PICKER_ONLY_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def picker_only_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', INPUT_ONLY_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def input_only_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', RADIO_ONLY_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def radio_only_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', CHECKBOX_ONLY_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def checkbox_only_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', ATTEMPT_PAGE_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def attempt_page_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', RUNNING_ATTEMPT_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def running_attempt_directory(directory: Path):
    return directory


@fixture
@pytest.mark.parametrize('directory', ALL_COURSES_PAGE_DIR.iterdir(), scope='session', ids=lambda param: param.name)
def all_courses_page_directory(directory: Path):
    return directory
