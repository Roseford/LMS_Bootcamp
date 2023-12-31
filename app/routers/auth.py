from fastapi import APIRouter, status, Depends, Response, HTTPException, Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2
from ..schemas.users import UserLogin, Email, ResponseMessage, CreateUser, SignIn, CheckPassword

router = APIRouter(tags=["Authentication"], prefix="/login")

@router.post('/', response_model=UserLogin)
def login(user_credentials: SignIn, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # CREATE AND RETURN A TOKEN
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    
    return {"access_token": access_token, "token_type": "bearer", "user": user}


@router.post('/change-password', response_model=ResponseMessage)
def change_password(password: CheckPassword, current_user: CreateUser = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):

    if password.new_password != password.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password mismatch")

    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    user.password = utils.hash_password(password.new_password)

    db.commit()

    return {"message": "Password updated successfully."}
