import re
from typing import List, Union
from urllib.parse import parse_qs, urlparse

import bs4
from loguru import logger

from src.moodle_api.models import (
    CourseRecord,
    TaskAttempt,
    TaskRecord,
    TaskSummaryPage,
    TaskTypes,
)
from src.utils import to_float, to_int


class PageParserBase:
    def __init__(self, page_url: str, page_content: bytes):
        self.page_url = page_url
        self.soup, self.content = (
            bs4.BeautifulSoup(page_content, features="lxml"),
            page_content,
        )

    def parse(self):
        raise NotImplementedError()


class TaskParserMixin:
    @staticmethod
    def _get_id(task_url: str) -> str:
        return parse_qs(urlparse(task_url).query)["id"][0]

    @staticmethod
    def _get_type(task_url: str) -> TaskTypes:
        for type_candidate in TaskTypes:
            if type_candidate.value in task_url:
                return type_candidate


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


class TaskSummaryParser(PageParserBase, TaskParserMixin):
    def parse(self) -> TaskSummaryPage:
        task_id, task_type = self._get_id(self.page_url), self._get_type(self.page_url)
        all_attempts = self.soup.find_all("tr")[1:]  # Первый - это хидер таблицы
        rv = []
        try:
            # Надо определить, где находится твоя оценка
            total_cols = all_attempts[0].find_all("td", {"class", "lastcol"})[0][
                "class"
            ]
            ide = [item for i, item in enumerate(total_cols) if re.search(r"c\d", item)]
            if ide:
                total_cols = int(ide[0][1:])
            # Если всего 2 колонки - то это status и урл
            # Если всего 4 колонки - то это статус, балл, оценка и урл
            for tag in all_attempts:
                score, mark = None, None
                order_num = tag.find("td", {"class": "c0"}).text
                status = tag.find("td", {"class": f"c1"}).text
                _fail_safe = tag.find("td", {"class": f"c{total_cols}"}).a
                if _fail_safe is None:
                    attempt_url = None
                else:
                    attempt_url = tag.find("td", {"class": f"c{total_cols}"}).a["href"]
                attempt_id = parse_qs(urlparse(attempt_url).query).get(
                    "attempt", [None]
                )[0]
                if total_cols == 4:
                    score = tag.find("td", {"class": f"c2"}).text.replace(",", ".")
                    mark = tag.find("td", {"class": f"c3"}).text.replace(",", ".")
                rv.append(
                    TaskAttempt(
                        number=order_num,
                        id=task_id,
                        type=task_type,
                        attempt_id=attempt_id,
                        score=to_float(score),
                        mark=to_float(mark),
                        status=status,
                    )
                )
            # BUG: best_attempt может указывать неоконченную попытку, если та единственна
        except IndexError:
            logger.info(
                "could not parse best own attempt. Proceeding as the first run..."
            )
        return TaskSummaryPage(id=to_int(task_id), type=task_type, attempts=rv)
