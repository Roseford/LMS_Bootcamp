from typing import Optional
from pydantic import BaseModel, EmailStr

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    phone: str

class UserOut(UpdateUser):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class CreateUser(UpdateUser):
    email: EmailStr
    password: str

class ResponseMessage(BaseModel):
    message: str

class UserLogin(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class Email(BaseModel):
    email: EmailStr

class TokenData(BaseModel):
    id: Optional[str] = None

class SignIn(BaseModel):
    email: EmailStr
    password: str