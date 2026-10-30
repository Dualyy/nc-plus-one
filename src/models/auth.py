from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class Login(BaseModel):
    email: str
    password: str


class CreateLogin(BaseModel):
    name: str
    email: str
    password: str


class Token(BaseModel):
    token: str
    type: str