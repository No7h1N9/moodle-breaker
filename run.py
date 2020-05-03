from moodle_api.auth import LoginManager
from moodle_api.problem import Task
from settings1 import LOGIN, PASSWORD, HOMEWORK_URLS, MEAN_URLS, MEAN_ATTEMPTS
import logging


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return -1


def setup_logger(loglevel):
    logger = logging.getLogger("main")
    logger.setLevel(loglevel)
    # create the logging file handler
    fh = logging.FileHandler("main.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = setup_logger(logging.DEBUG)


def cheat_on(url, multiple=1):
    with LoginManager(login=LOGIN, password=PASSWORD) as session:
        task = Task(task_url=url, session=session)
        logger.info(f'starting task {task.task_url}')
        for _ in range(multiple):
            try:
                task.break_it()
            except Exception as e:
                logger.debug(f'cookies: {session.cookies}')
                logger.error(e, stack_info=True)
                raise e


if __name__ == '__main__':
    for url in HOMEWORK_URLS:
        cheat_on(url)
    for url in MEAN_URLS:
        cheat_on(url, multiple=MEAN_ATTEMPTS)
