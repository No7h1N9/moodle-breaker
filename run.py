from moodle_api.auth import LoginManager
from moodle_api.problem import Task
from settings1 import LOGIN, PASSWORD, HOMEWORK_URLS, MEAN_URLS, MEAN_ATTEMPTS

from utils import logger


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
