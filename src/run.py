import os

from network import MoodleAPI
from parsers import TaskMetadata

from src.moodle_api import FinishedAttemptPage, RunningAttemptPage, SummaryPage
from utils import logger

"""
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
"""


def cheat_on():
    api = MoodleAPI(
        login=os.environ.get("MOODLE_LOGIN"), password=os.environ.get("MOODLE_PASSWORD")
    )
    cmid = "30887"
    response = api.get_summary_page(cmid=cmid)
    best_attempt = SummaryPage(response.content).best_attempt_id()
    response = api.get_finished_attempt_page(cmid, best_attempt)
    answers = FinishedAttemptPage(response.content).parse_answers()
    metadata = TaskMetadata(response.content)
    # attempt_id, prefix = api.start_attempt(cmid, metadata.sesskey)
    response = api.start_attempt(cmid, metadata.sesskey)
    attempt = RunningAttemptPage(response.content)
    missing_answers = attempt.all_questions.difference(set(answers.keys()))
    if missing_answers:
        logger.warning(
            "Missing answers for fields: {}".format(", ".join(missing_answers))
        )

    api.upload_answers(cmid, metadata.sesskey, attempt.id, attempt.prefix, answers)
    api.finish_attempt(cmid, metadata.sesskey, attempt.id)


if __name__ == "__main__":
    cheat_on()
