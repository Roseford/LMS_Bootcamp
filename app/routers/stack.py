from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..models import Courses, User
from .. import database, oauth2
from ..schemas.stack import CourseOut, Stack, GetAssignment
from ..schemas.users import ResponseMessage, CreateUser
from typing import List


router = APIRouter(tags=["stack"], prefix="/stack")

stacks = [
 {
  "name": "Product Design",
  "courses": [
   {"title": "UI/UX", "course_code": "001"},
   {"title": "DesignOps", "course_code": "002"}
  ],
  "id": 1
 },
 {
  "name": "Frontend",
  "courses": [
   {"title": "Mobile", "course_code": "003"},
   {"title": "Web", "course_code": "004"}
  ],
  "id":  2
 },
 {
  "name": "Management",
  "courses": [
   {"title": "Product Management", "course_code": "005"},
   {"title": "Project Management", "course_code": "006"}
  ],
  "id": 3
 },
 {
  "name": "Backend",
  "courses": [
   {"title": "NodeJs/Express.js", "course_code": "007"},
   {"title": "Python/Django", "course_code": "008"}
  ],
  "id": 4
 }
]

@router.get("/", response_model=List[Stack])
def get_stack_and_courses():
    return stacks

@router.post("/course/{course_code}", response_model=ResponseMessage)
def add_course(course_code: str, db: Session = Depends(database.get_db), current_user: CreateUser = Depends(oauth2.get_current_user)):
    '''
    get the course_code from the course_code field in each course
    ''' 
    course_db = db.query(Courses).filter(Courses.course_code == course_code, Courses.user_id == current_user.id).first()

    if course_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course has already been registered")

    new_course = None
    stack_name = None

    for stack in stacks:
        for course in stack["courses"]:
            if course["course_code"] == course_code:
                new_course = course
                stack_name = stack["name"]

    if not new_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course does not exist")

    new_db_course = Courses(**new_course, stack=stack_name, user_id=current_user.id)
    db.add(new_db_course)
    db.commit()

    return {"message": "Course has been added successfully"}

@router.get("/course", response_model=List[CourseOut])
def get_current_user_courses(db: Session = Depends(database.get_db), current_user: CreateUser = Depends(oauth2.get_current_user)):
    '''
    get the course_code from the course_code field in each course
    ''' 
    courses = db.query(Courses).filter(Courses.user_id == current_user.id).all()

    return courses

@router.get("/assignment", response_model=List[GetAssignment])
def get_assignment():
    assignment = [
        {
            "name": "Developing Restaurant Apis",
            "stack": "Backend",
            "time": "08:00 AM",
            "date": "23/06"
        },
        {
            "name": "Developing Restaurant Apis",
            "stack": "Backend",
            "time": "08:00 AM",
            "date": "23/06"
        },
        {
            "name": "Developing Restaurant Apis",
            "stack": "Backend",
            "time": "08:00 AM",
            "date": "23/06"
        }
    ]
    return assignment


@router.delete("/course/{course_code}", response_model=ResponseMessage)
def delete_course(course_code: str, db: Session = Depends(database.get_db), current_user: CreateUser = Depends(oauth2.get_current_user)):
    '''
    get the course_code from the course_code field in each course
    ''' 
    course_db = db.query(Courses).filter(Courses.course_code == course_code, Courses.user_id == current_user.id).first()

    if not course_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course does not exist")
    
    db.query(Courses).filter(Courses.course_code == course_code, Courses.user_id == current_user.id).delete()
    db.commit()

    return {"message": "Course has been deleted successfully"}



