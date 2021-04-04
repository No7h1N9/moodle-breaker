import os

from dotenv import load_dotenv


def correct_auth_env_login_password():
    load_dotenv()
    return os.environ.get("MOODLE_TEST_LOGIN"), os.environ.get("MOODLE_TEST_PASSWORD")
