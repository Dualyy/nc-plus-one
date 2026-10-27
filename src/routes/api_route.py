from fastapi import APIRouter, FastAPI,HTTPException
from pydantic import BaseModel
from psycopg.rows import dict_row 
from datetime import datetime

from src.connection import get_connection

api_router=APIRouter(prefix="/api")

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


@api_router.post("/auth/login", status_code= 200)
def submit_auth(login: Login) -> Token:
    """attempt to login
    
    requires email and password fields
    raises status 401 in login invalid
    and 400 if misformed
    """
    if login.password and login.email:
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
        return Token(token=token)
    elif(login.email and not login.password) or (login.password and not login.email):
        raise HTTPException(status_code=400,detail={"status_code": "400 BAD REQUEST",
                                                                    "msg": "Missing email or password field"})


@api_router.post("/auth/register", status_code=201, response_model=User)
def register_user(login_info: CreateLogin):
    if not login_info:
        raise HTTPException(status_code=400,detail={"status_code": "400 BAD REQUEST",
                                                                    "msg": f"Field required"})
    pass
    conn = get_connection()
    with conn.cursor(row_factory=dict_row) as crsr:
        crsr.execute("""SELECT * FROM users
                        WHERE email = %s;
                         """,(login_info.email,))
        login = list(crsr.fetchall())
        if len(login) > 0:
            raise HTTPException(status_code=400,detail={"status_code": "400 BAD REQUEST",
                                                        "msg": f"A user with email {login_info.email} already exists"})

        crsr.execute("""INSERT INTO users(name,email,password)
                        VALUES (%s,%s,%s)
                        RETURNING *;
                    """,(login_info.name,login_info.email,login_info.password))
        conn.commit()
        user = crsr.fetchone()
        created_at = user['created_at']
        print(created_at)
        user.pop('created_at')
        return User(**user, created_at=created_at)