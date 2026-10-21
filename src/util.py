import json
import psycopg
from src.connection import get_connection
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_json_file(filepath):
    with open(filepath) as f:
        for row in json.load(f):
            yield row


def drop_user_table(conn: psycopg.connection):
    """execute to drop the user table"""
    logger.info("DROPPING TABLE user")
    try:
        with conn.cursor() as curs:
            curs.execute("""DROP TABLE IF EXISTS users""")
            conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")


def insert_user_data(conn: psycopg.connection, filepath):
    """execute to insert user data from .JSON file"""
    try:
        data = load_json_file(filepath)
        insert_statement = (
            "INSERT INTO users (email, password, name) VALUES (%s, %s, %s);"
        )
        with conn.cursor() as curs:
            for row in data:
                curs.execute(
                    insert_statement, (row["email"], row["password"], row["name"])
                )
        conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")


def create_user_table(conn: psycopg.connection):
    """create user table"""
    drop_user_table(conn)
    logger.info("CREATE TABLE users")
    with conn.cursor() as curs:
        curs.execute("""CREATE TABLE users(
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT now()
                        );""")
        conn.commit()

