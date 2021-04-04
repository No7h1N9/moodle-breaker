import bs4
import re
from enum import Enum
from typing import Union, List
from pydantic import BaseModel


class HtmlParsable:

    @classmethod
    def from_content(cls, page_content: bytes) -> Union['HtmlParsable', List['HtmlParsable']]:
        raise NotImplementedError()


class CourseRecord(BaseModel, HtmlParsable):
    name: str
    course_id: str
    mark: str

    @classmethod
    def from_content(cls, page_content: bytes) -> Union['CourseRecord', List['CourseRecord']]:
        soup, content = bs4.BeautifulSoup(page_content, features='lxml'), page_content
        rv = []
        raw_courses = soup.find('table', {'id': 'overview-grade'}).find('tbody').\
            find_all('tr', {'class': lambda x: x != "emptyrow"})
        for row in raw_courses:
            link_tag, mark_tag, _ = list(row.children)
            course_name = link_tag.find('a').text.strip()
            course_id = re.search(r'id=(\d+)', link_tag.find('a')['href'].strip()).groups()[0]
            mark = mark_tag.text.strip()
            rv.append(CourseRecord(name=course_name, course_id=course_id, mark=mark))
        return rv


class TaskTypes(Enum):
    QUIZ = 'quiz'
    FORUM = 'forum'
    WRITING = 'assign'


class TaskBase(BaseModel):
    type: TaskTypes
    id: int


class TaskRecord(TaskBase, HtmlParsable):

    percentage: float = 0.

    @staticmethod
    def _get_id(task_tag: bs4.Tag) -> str:
        task_url = task_tag['href']
        return re.search(r'\Wid=(\d+)', task_url).groups()[0]

    @staticmethod
    def _get_type(task_tag: bs4.Tag) -> TaskTypes:
        task_url = task_tag['href']
        for type_candidate in TaskTypes:
            if type_candidate.value in task_url:
                return type_candidate

    @staticmethod
    def _get_percentage(task_tag: bs4.Tag) -> float:
        tr = task_tag.parent
        while tr.name != 'tr':
            tr = tr.parent
        results = tr.find_all('td', {'headers': 'percentage'})
        assert len(results) == 1
        percentage_row = results[0]
        if percentage_row.text == '-':
            return 0.
        return float(re.findall(r'\d+[,.]?\d+', percentage_row.text)[0].replace(',', '.'))

    @classmethod
    def from_content(cls, page_content: bytes) -> Union['TaskRecord', List['TaskRecord']]:
        soup, content = bs4.BeautifulSoup(page_content, features='lxml'), page_content
        rv = []
        for task_tag in soup.find_all('a', {'class': 'gradeitemheader'}):
            task_id = TaskRecord._get_id(task_tag)
            task_type = TaskRecord._get_type(task_tag)
            task_percentage = TaskRecord._get_percentage(task_tag)
            rv.append(TaskRecord(type=task_type, id=task_id, percentage=task_percentage))
        return rv


