import json
from typing import Any, Tuple

from src.moodle_api.models import TaskAttempt


def load_fixture(directory) -> Tuple[str, str, Any]:
    with open(directory / "index.htm") as page:
        with open(directory / "params.json") as params:
            params = json.loads(params.read())
            return page.read(), params["url"], params


def load_summary_fixture(directory) -> Tuple[str, str, Any]:
    page, url, params = load_fixture(directory)
    params["payload"]["attempts"] = [
        TaskAttempt(**value) for value in params["payload"]["attempts"]
    ]
    return page, url, params


def case_finished_task_picker_only(picker_only_directory):
    return load_fixture(picker_only_directory)


def case_finished_task_input_only(input_only_directory):
    return load_fixture(input_only_directory)


def case_finished_task_radio_only(radio_only_directory):
    return load_fixture(radio_only_directory)


def case_finished_task_checkbox_only(checkbox_only_directory):
    return load_fixture(checkbox_only_directory)


def case_attempt_page_various_attempt_pages(attempt_page_directory):
    return load_summary_fixture(attempt_page_directory)


def case_running_attempt_various_types(running_attempt_directory):
    return load_fixture(running_attempt_directory)
