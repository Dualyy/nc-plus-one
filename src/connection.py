from dotenv import dotenv_values
import os
import psycopg

os.environ["ENV"] = "test"


def get_connection():
    config = dotenv_values(f".env.{os.getenv('ENV')}")
    connection = psycopg.connect(**config)
    return connection
