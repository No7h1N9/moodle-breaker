from moodle_api.auth import LoginManager


def test_get_login_token(login_manager: LoginManager):
    assert login_manager.login_token


def test_is_authorized_after_login(login_manager: LoginManager):
    assert not login_manager.is_authorized
    login_manager.authorize()
    assert login_manager.is_authorized


def test_context_manager(login_manager: LoginManager):
    with login_manager:
        assert login_manager.is_authorized
