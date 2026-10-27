from fastapi import APIRouter, FastAPI,HTTPException
from pydantic import BaseModel

from src.connection import get_connection

api_router=APIRouter(prefix="/api")


class Login(BaseModel):
    email: str
    password: str

@api_router.post("/auth/login", status_code= 200)
def submit_auth(login: Login):
    if login:
        conn = get_connection()
        with conn.cursor() as crsr:
            crsr.execute("""SELECT * FROM users
                            WHERE email = %s AND password = %s;
                            """,(login.email,login.password,))
            login_details =  crsr.fetchall()
            print(login.email, login.password)
            if login_details == []:
                raise HTTPException(status_code=401,detail={"status_code": "401 UNAUTHORIZED",
                                                                    "msg": "email or password wrong"})
            token = ""
        return {"token" :token}
    else:
        raise HTTPException(status_code=401,detail={"status_code": "401 UNAUTHORIZED",
                                                                    "msg": "email or password wrong"})