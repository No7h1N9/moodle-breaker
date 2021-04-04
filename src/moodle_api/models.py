from enum import Enum

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
