from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

api_router=APIRouter(prefix="/api")


class Login(BaseModel):
    email: str
    password: str

@api_router.post("/auth/login", status_code= 200)
def submit_auth(login: Login):
    
    token = ""
    return {"token" :token}