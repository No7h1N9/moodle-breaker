from dotenv import load_dotenv
import os


def correct_env_login_password():
    load_dotenv()
    return os.environ.get('MOODLE_TEST_LOGIN'), os.environ.get('MOODLE_TEST_PASSWORD')
