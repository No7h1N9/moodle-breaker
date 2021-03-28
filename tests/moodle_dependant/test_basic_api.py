from pytest_cases import parametrize_with_cases
from src.moodle_api.network import MoodleAPI


@parametrize_with_cases('login, password', prefix='correct_')
def test_correct_auth_status_after_login(login, password):
    api = MoodleAPI(login, password)
    api.auth()
    assert api.is_authorized
