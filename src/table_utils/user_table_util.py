import json
from fastapi import HTTPException
import psycopg
from psycopg.rows import dict_row
from src.connection import get_connection
import logging
from src.util import load_json_file
from src.auth.passwords import hash_password

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_user(conn: psycopg.Connection, email: str):
    """retrieves the user by email
    takes a psycopg.Connection and user email as str"""
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            """SELECT * FROM users
                        WHERE email = %s
                        """,
            (email,),
        )
        user = curs.fetchone()
    if user == None:
        raise HTTPException(
            status_code=400,
            detail={"status_code": "400 BAD REQUEST", "msg": f"INVALID REQUEST"},
        )
    return user


def get_user_by_id(id: int):
    """retrieves the user by a user_id
    This function is used for retrieving a login user it deliberately throws a 400
    to obscure whether or not an account with this email already exists."""
    conn = get_connection()
    with conn.cursor(row_factory=dict_row) as curs:
        curs.execute(
            """SELECT * FROM users
                        WHERE id = %s
                        """,
            (id,),
        )
        user = curs.fetchone()
    if user == None:
        
        raise HTTPException(
            status_code=400,
            detail={"status_code": "400 BAD REQUEST", "msg": f"INVALID REQUEST"},
        )
    return user


def drop_user_table(conn: psycopg.Connection):
    """execute to drop the user table"""
    logger.info("DROPPING TABLE user")
    try:
        with conn.cursor() as curs:
            curs.execute("""DROP TABLE IF EXISTS users""")
            conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")
    logger.info("Users table dropped")


def insert_user_data(conn: psycopg.Connection, filepath):
    """execute to insert user data from .JSON file"""
    try:
        data = load_json_file(filepath)
        insert_statement = (
            "INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s);"
        )
        logging.info(f"inserting data from '{filepath}' into users")
        with conn.cursor() as curs:
            for row in data:
                curs.execute(
                    insert_statement,
                    (row["email"], hash_password(row["password"]), row["name"]),
                )
        conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")
    logging.info(f"data inserted into users")


def create_user_table(conn: psycopg.Connection):
    """create user table"""
    logger.info("CREATE TABLE users")
    with conn.cursor() as curs:
        curs.execute("""CREATE TABLE users(
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT now()
                        );""")
        conn.commit()
    logger.info("Users table created")
