from enum import Enum
from typing import List

from pydantic import BaseModel


class CourseRecord(BaseModel):
    """Запись о каждом курсе на странице с оценками.

    Moodle page: "Главная" -> "Оценки"
    """

    name: str
    course_id: str
    mark: str


class TaskTypes(Enum):
    """Известные типы заданий."""

    # Красная иконка, BREAKABLE
    QUIZ = "quiz"
    # Ответ писать на форуме. NOT BREAKABLE по природе
    FORUM = "forum"
    # Ответ в развернутой форме. NOT BREAKABLE по природе
    WRITING = "assign"


class TaskBase(BaseModel):
    """Базовая инфа о задании: тип и id."""

    type: TaskTypes
    id: int


class TaskRecord(TaskBase):
    """Запись о задании в большой странице с оценками.

    Moodle page: "Главная" -> "Оценки" -> (выбрать любой курс)
    """

    percentage: float = 0.0


class TaskAttempt(TaskBase):
    status: str
    attempt_id: str = None
    score: float = None
    mark: float = None
    MAX_MARK: float = 10.0


class TaskSummaryPage(TaskBase):
    best_attempt: TaskAttempt = None
    attempts: List[TaskAttempt]
