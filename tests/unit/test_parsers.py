from pytest_cases import parametrize_with_cases

from src.moodle_api.pages import (FinishedAttemptPage, RunningAttemptPage,
                                  SummaryPage)
from src.moodle_api.parsers import TaskMetadata


@parametrize_with_cases("page_content, task_metadata", prefix="case_attempt_page_")
def test_find_best_own_url(page_content, task_metadata):
    parser = SummaryPage(page_content)
    assert parser.best_attempt_id() == task_metadata["best_attempt_id"]


@parametrize_with_cases("page_content, task_metadata", prefix="case_finished_task_")
def test_parse_answers(page_content, task_metadata):
    parser = FinishedAttemptPage(page_content)
    assert parser.parse_answers() == task_metadata["answers"]


@parametrize_with_cases("page_content, task_metadata")
def test_parse_task_metadata(page_content, task_metadata):
    mt = TaskMetadata(page_content)
    assert mt.cmid == task_metadata["cmid"]
    assert mt.sesskey == task_metadata["sesskey"]


@parametrize_with_cases("page_content, task_metadata", prefix="case_running_attempt_")
def test_parse_questions(page_content, task_metadata):
    parser = RunningAttemptPage(page_content)
    assert parser.id == task_metadata["attempt_id"]
    assert parser.prefix == task_metadata["prefix"]
    assert parser.all_questions == set(task_metadata["questions"])
