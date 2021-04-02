from typing import Any, Tuple
from src.moodle_api.models import CourseRecord
import json


def load_fixture(directory) -> Tuple[str, Any]:
    with open(directory / 'index.htm') as page:
        with open(directory / 'params.json') as params:
            return page.read(), {key: CourseRecord(**value) for key, value in json.loads(params.read()).items()}


def case_all_courses_all_fixtures(all_courses_page_directory):
    return load_fixture(all_courses_page_directory)
