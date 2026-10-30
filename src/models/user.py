from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    name: str
    created_at: datetime


class TokenUser(BaseModel):
    id: int
    name: str
