from pytest_cases import parametrize_with_cases

from src.moodle_api.page_parsers import TaskSummaryParser
from src.moodle_api.pages import FinishedAttemptPage, RunningAttemptPage
from src.moodle_api.parsers import TaskMetadata


@parametrize_with_cases(
    "page_content, page_url, task_metadata", prefix="case_attempt_page_"
)
def test_find_best_own_url(page_content, page_url, task_metadata):
    parser = TaskSummaryParser(page_content=page_content, page_url=page_url).parse()
    assert parser.attempts == task_metadata["payload"]["attempts"]


@parametrize_with_cases(
    "page_content, page_url, task_metadata", prefix="case_finished_task_"
)
def test_parse_answers(page_content, page_url, task_metadata):
    parser = FinishedAttemptPage(page_content)
    assert parser.parse_answers() == task_metadata["answers"]


@parametrize_with_cases("page_content, page_url, task_metadata")
def test_parse_task_metadata(page_content, page_url, task_metadata):
    mt = TaskMetadata(page_content)
    print(task_metadata)
    assert mt.cmid == task_metadata["network"]["cmid"]
    assert mt.sesskey == task_metadata["network"]["sesskey"]


@parametrize_with_cases(
    "page_content, page_url, task_metadata", prefix="case_running_attempt_"
)
def test_parse_questions(page_content, page_url, task_metadata):
    parser = RunningAttemptPage(page_content)
    assert parser.id == task_metadata["attempt_id"]
    assert parser.prefix == task_metadata["prefix"]
    assert parser.all_questions == set(task_metadata["questions"])
