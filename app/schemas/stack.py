from pydantic import BaseModel

class StackCourse(BaseModel):
    title: str
    course_code: str

class CourseOut(StackCourse):
    id: int
    stack: str
    user_id: int

    class Config():
        orm_mode = True

class Stack(BaseModel):
    name: str
    id: int
    courses: list[StackCourse]

class GetAssignment(BaseModel):
    name: str
    stack: str
    time: str
    date: str