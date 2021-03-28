from typing import Any, Tuple
import json


def load_fixture(directory) -> Tuple[str, Any]:
    with open(directory / 'index.htm') as page:
        with open(directory / 'params.json') as params:
            return page.read(), json.loads(params.read())


def case_finished_task_picker_only(picker_only_directory):
    return load_fixture(picker_only_directory)


def case_finished_task_input_only(input_only_directory):
    return load_fixture(input_only_directory)


def case_finished_task_radio_only(radio_only_directory):
    return load_fixture(radio_only_directory)


def case_finished_task_checkbox_only(checkbox_only_directory):
    return load_fixture(checkbox_only_directory)


def case_attempt_page_various_attempt_pages(attempt_page_directory):
    return load_fixture(attempt_page_directory)


def case_running_attempt_various_types(running_attempt_directory):
    return load_fixture(running_attempt_directory)
