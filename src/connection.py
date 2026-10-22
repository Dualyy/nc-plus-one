from dotenv import dotenv_values
import os
import psycopg

ENV = "development"


def get_connection():
    config = dotenv_values(f".env.{ENV}")
    connection = psycopg.connect(**config)
    return connection
