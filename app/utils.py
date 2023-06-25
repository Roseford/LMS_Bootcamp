from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

'''Takes a string hashes it and returns it'''
def hash_password(password: str):
    return password_context.hash(password)

'''Verifies the password by hashing the new string'''
def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
