from pytest_cases import parametrize_with_cases
from src.moodle_api.pages import AllCoursesPage
from src.moodle_api.models import TaskRecord


@parametrize_with_cases('page_content, expected_data', prefix='case_all_courses_')
def test_all_courses_page_is_parsed_correctly(page_content, expected_data):
    parser = AllCoursesPage(page_content)
    assert parser.all_courses() == expected_data


@parametrize_with_cases('page_content, expected_data', prefix='case_all_tasks_for_course_')
def test_all_tasks_page_is_parsed_correctly(page_content, expected_data):
    records = TaskRecord.from_content(page_content)
    assert len(records) == expected_data['total_tasks']
    assert records == expected_data['parsed_tasks']
