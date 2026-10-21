import psycopg
from src.connection import get_connection
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_venues_table(conn: psycopg.connection):
    """create venues table"""
    logger.info("CREATE TABLE venues")
    with conn.cursor() as curs:
        curs.execute("""CREATE TABLE venues(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        address TEXT,
                        capacity IN
                    );""")
        conn.commit()
    logger.info("Venues table created")


def drop_venues_table(conn: psycopg.connection):
    """create venues table"""
    logger.info("DROPPING TABLE venues")
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS venues""")
        conn.commit()
    logger.info("Venues table dropped")

def insert_venues_data(conn: psycopg.connection):
    
    pass