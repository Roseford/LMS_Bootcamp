from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String, nullable=False, unique=False)
    lastname = Column(String, nullable=False, unique=False)
    phone = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

     # Define the relationship to courses
    courses = relationship("Courses", back_populates="user")
    
class Courses(Base):
    __tablename__= "courses"

    id = Column(Integer, primary_key=True, nullable=False)
    stack = Column(String, nullable=False)
    title = Column(String, nullable=False, unique=False)
    course_code = Column(String, nullable=False, unique=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Define the relationship to the user
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="courses")

# class ForgotPassword(Base):
#     __tablename__ = "forgotPassword"

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     reset_code = Column(String,nullable=False, unique=True)
#     expires_in = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
