from pytest_cases import parametrize_with_cases
from src.moodle_api.pages import AllCoursesPage


@parametrize_with_cases('page_content, expected_data', prefix='case_all_courses_')
def test_all_courses_page_is_parsed_correctly(page_content, expected_data):
    parser = AllCoursesPage(page_content)
    assert parser.all_courses() == expected_data
