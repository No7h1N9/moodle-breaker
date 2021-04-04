import json
from typing import Any, Tuple

from src.moodle_api.models import CourseRecord, TaskRecord


def load_course_record_fixture(directory) -> Tuple[str, Any]:
    with open(directory / "index.htm") as page:
        with open(directory / "params.json") as params:
            return page.read(), {
                key: CourseRecord(**value)
                for key, value in json.loads(params.read()).items()
            }


def load_fixture(directory) -> Tuple[str, Any]:
    with open(directory / "index.htm") as page:
        with open(directory / "params.json") as params:
            expected_data = json.loads(params.read())
            # Parse to classes
            expected_data["parsed_tasks"] = [
                TaskRecord(**data) for data in expected_data["parsed_tasks"]
            ]
            return page.read(), expected_data


def case_all_courses_all_fixtures(all_courses_page_directory):
    return load_course_record_fixture(all_courses_page_directory)


def case_all_tasks_for_course_all_fixtures(all_tasks_page_directory):
    return load_fixture(all_tasks_page_directory)
