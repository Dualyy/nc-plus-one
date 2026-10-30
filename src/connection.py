import psycopg
from dotenv import dotenv_values
import os


def get_environment() -> str:
    return os.getenv("ENV", "development")  # one source of truth

config = dotenv_values(f".env.{get_environment()}")

def get_connection():
    

    conn_string = psycopg.conninfo.make_conninfo(
        host=config.get('HOST'),
        dbname=config.get('DBNAME'),
        user=config.get('USER'),
        password=config.get('PASSWORD'),
        port=config.get('PORT', '5432')
    )
    return psycopg.connect(conninfo=conn_string)