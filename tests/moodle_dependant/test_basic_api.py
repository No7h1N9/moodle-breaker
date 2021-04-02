from pytest_cases import parametrize_with_cases, fixture
from src.moodle_api.network import MoodleAPI


@fixture
@parametrize_with_cases('login, password', prefix='correct_auth_')
def moodle_api(login, password) -> MoodleAPI:
    yield MoodleAPI(login, password)


def test_correct_auth_status_after_login(moodle_api: MoodleAPI):
    moodle_api.auth()
    assert moodle_api.is_authorized


def test_get_my_courses_returns_correct_page(moodle_api: MoodleAPI):
    assert 'Курсы, на которых я учусь' in moodle_api.get_my_courses().text
