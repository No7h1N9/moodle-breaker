from pytest_cases import parametrize_with_cases

from src.moodle_api.page_parsers import CourseRecordsParser, TaskRecordParser


@parametrize_with_cases(
    "page_content, page_url, expected_data", prefix="case_all_courses_"
)
def test_all_courses_page_is_parsed_correctly(page_content, page_url, expected_data):
    records = CourseRecordsParser(page_content=page_content, page_url=page_url).parse()
    assert records == expected_data


@parametrize_with_cases(
    "page_content, page_url, expected_data", prefix="case_all_tasks_for_course_"
)
def test_all_tasks_page_is_parsed_correctly(page_content, page_url, expected_data):
    records = TaskRecordParser(page_url=page_url, page_content=page_content).parse()
    assert len(records) == expected_data["total_tasks"]
    assert records == expected_data["parsed_tasks"]
