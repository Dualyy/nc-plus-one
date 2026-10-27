import psycopg
import logging
from src.util import load_json_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#TODO: fix doc strings
def create_venues_table(conn: psycopg.connection):
    """The function takes a psycopg connection and tries to create a venues table"""
    logger.info("CREATE TABLE venues")
    with conn.cursor() as curs:
        try:
            curs.execute("""CREATE TABLE venues(
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            address TEXT,
                            capacity INT
                        );""")
            conn.commit()
            logger.info("Venues table created")
        except psycopg.errors.DuplicateTable:
            logging.warning("venues table already exists")


def drop_venues_table(conn: psycopg.connection):
    """The function takes a psycopg connection and drops the venues table if it exists"""
    logger.info("DROPPING TABLE venues")
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS venues""")
        conn.commit()
    logger.info("Venues table dropped")


def insert_venues_data(conn: psycopg.connection, filepath):
    """The function takes a psycopg connection and a file path.
    It insert venue data from .JSON file. File requires each object to have a 'name', 'address', and 'capacity' key.
    """

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
