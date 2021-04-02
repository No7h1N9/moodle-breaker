from pydantic import BaseModel


class CourseRecord(BaseModel):
    name: str
    course_id: str
    mark: str
