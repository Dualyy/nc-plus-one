import psycopg
import logging
from src.util import load_json_file

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
                        capacity INT
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


def insert_venues_data(conn: psycopg.connection, filepath):
    """execute to insert user data from .JSON file"""
    logging.info(f"inserting data from '{filepath}' into venues")
    try:
        data = load_json_file(filepath)
        insert_statement = (
            "INSERT INTO venues (name, address, capacity) VALUES (%s, %s, %s);"
        )
        with conn.cursor() as curs:
            for row in data:
                curs.execute(
                    insert_statement, (row["name"], row["address"], row["capacity"])
                )
        conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")
    logging.info(f"data inserted into venues")
