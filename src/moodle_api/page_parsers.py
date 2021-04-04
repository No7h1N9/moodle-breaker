import re
from typing import List, Union
from urllib.parse import parse_qs, urlparse

import bs4

from src.moodle_api.models import CourseRecord, TaskRecord, TaskTypes


class PageParserBase:
    def __init__(self, page_url: str, page_content: bs4.BeautifulSoup):
        self.page_url = page_url
        self.soup, self.content = (
            bs4.BeautifulSoup(page_content, features="lxml"),
            page_content,
        )

    def parse(self):
        raise NotImplementedError()


class CourseRecordsParser(PageParserBase):
    def parse(self) -> Union["CourseRecord", List["CourseRecord"]]:
        rv = []
        raw_courses = (
            self.soup.find("table", {"id": "overview-grade"})
            .find("tbody")
            .find_all("tr", {"class": lambda x: x != "emptyrow"})
        )
        for row in raw_courses:
            link_tag, mark_tag, _ = list(row.children)
            course_name = link_tag.find("a").text.strip()
            course_id = re.search(
                r"id=(\d+)", link_tag.find("a")["href"].strip()
            ).groups()[0]
            mark = mark_tag.text.strip()
            rv.append(CourseRecord(name=course_name, course_id=course_id, mark=mark))
        return rv


class TaskParserMixin:
    @staticmethod
    def _get_id(task_url: str) -> str:
        return parse_qs(urlparse(task_url).query)["id"][0]

    @staticmethod
    def _get_type(task_url: str) -> TaskTypes:
        for type_candidate in TaskTypes:
            if type_candidate.value in task_url:
                return type_candidate


class TaskRecordParser(PageParserBase, TaskParserMixin):
    @staticmethod
    def _get_percentage(task_tag: bs4.Tag) -> float:
        tr = task_tag.parent
        while tr.name != "tr":
            tr = tr.parent
        results = tr.find_all("td", {"headers": "percentage"})
        assert len(results) == 1
        percentage_row = results[0]
        if percentage_row.text == "-":
            return 0.0
        return float(
            re.findall(r"\d+[,.]?\d+", percentage_row.text)[0].replace(",", ".")
        )

    def parse(self) -> List["TaskRecord"]:
        rv = []
        for task_tag in self.soup.find_all("a", {"class": "gradeitemheader"}):
            task_id = self._get_id(task_tag["href"])
            task_type = self._get_type(task_tag["href"])
            task_percentage = self._get_percentage(task_tag)
            rv.append(
                TaskRecord(type=task_type, id=task_id, percentage=task_percentage)
            )
        return rv
