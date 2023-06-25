from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import users
from app.routers import auth
from app.routers import stack


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(stack.router)
