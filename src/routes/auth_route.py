from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row
from src.table_utils.user_table_util import get_user
from src.auth.security import create_JWT_token
from src.auth.passwords import verify_password, hash_password
from src.models.auth import *

from src.connection import get_connection

auth_router = APIRouter(prefix="/auth")





@auth_router.post("/login", status_code=200)
def submit_auth(login: Login) -> Token:
    """attempt to login

    requires email and password fields
    raises status 401 in login invalid
    and 400 if misformed
    """

    conn = get_connection()
    if login.password and login.email:
        user = get_user(conn, login.email)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail={
                    "status_code": "401 UNAUTHORIZED",
                    "msg": "email or password wrong",
                },
            )
        if verify_password(user["password_hash"], login.password):
            token = create_JWT_token(user["id"], user["name"])
            return Token(token=token, type="bearer")
        else:
            raise HTTPException(
                status_code=401,
                detail={
                    "status_code": "401 UNAUTHORIZED",
                    "msg": "email or password wrong",
                },
            )

    else:
        raise HTTPException(
            status_code=400,
            detail={
                "status_code": "400 BAD REQUEST",
                "msg": "Missing email or password field",
            },
        )


@auth_router.post("/register", status_code=201, response_model=User)
def register_user(login_info: CreateLogin):
    if not login_info:
        raise HTTPException(
            status_code=400,
            detail={"status_code": "400 BAD REQUEST", "msg": f"Field required"},
        )
    pass
    conn = get_connection()
    with conn.cursor(row_factory=dict_row) as crsr:
        crsr.execute(
            """SELECT * FROM users
                        WHERE email = %s;
                         """,
            (login_info.email,),
        )
        login = crsr.fetchone()
        if login != None:
            raise HTTPException(
                status_code=400,
                detail={
                    "status_code": "400 BAD REQUEST",
                    "msg": f"A user with email {login_info.email} already exists",
                },
            )

        crsr.execute(
            """INSERT INTO users(name,email,password_hash)
                        VALUES (%s,%s,%s)
                        RETURNING *;
                    """,
            (login_info.name, login_info.email, hash_password(login_info.password)),
        )
        conn.commit()
        user = crsr.fetchone()
        created_at = user["created_at"]
        user.pop("created_at")
        return User(**user, created_at=created_at)
