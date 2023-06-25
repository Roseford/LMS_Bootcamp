from fastapi import APIRouter, status, Depends, Response, HTTPException
from app.schemas.users import CreateUser, UserOut, ResponseMessage, UpdateUser
from .. import models, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=["users"], prefix="/users")

'''Hashes the password, a string'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseMessage)
def create_user(user: CreateUser, db: Session = Depends(get_db)):

    user_phone = db.query(models.User).filter(models.User.phone == user.phone).first()
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_phone:
        raise HTTPException(status_code=400, detail="Phone Number already registered")
    
    if user_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_password = utils.hash_password(user.password)
    user.password = hash_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Account successfully created"}

@router.get("/user-detail", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_current_user(current_user: CreateUser = Depends(oauth2.get_current_user)):
    return current_user

@router.patch("/", status_code=status.HTTP_200_OK, response_model=ResponseMessage)
def update_user(user: UpdateUser, current_user: CreateUser = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == current_user.email).first()
        # Update the user's details
    db_user.firstname = user.firstname
    db_user.lastname = user.lastname
    db_user.phone = user.phone

    db.commit()

    return {"message": "Profile successfully updated"}

