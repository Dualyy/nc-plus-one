import psycopg
from dotenv import dotenv_values
import os


def get_environment() -> str:
    """
    Get the environment variable and set it to development by default if none was given

    """
    return os.getenv("ENV", "development")


config = dotenv_values(f".env.{get_environment()}")


def get_connection():
    """
    use this to establish the database connection with the environment data from the
    environment set/ retrieved by get_environment

    returns psycopg.Connection
    """
    conn_string = psycopg.conninfo.make_conninfo(
        host=config.get("HOST"),
        dbname=config.get("DBNAME"),
        user=config.get("USER"),
        password=config.get("PASSWORD"),
        port=config.get("PORT", "5432"),
    )
    return psycopg.connect(conninfo=conn_string)
