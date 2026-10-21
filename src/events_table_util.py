import psycopg
import logging
from src.util import load_json_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_events_table(conn: psycopg.connection):
    """create events table"""
    logger.info("CREATE TABLE events")
    with conn.cursor() as curs:
        curs.execute("""CREATE TABLE events(
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description VARCHAR(255),
                        starts_at TIMESTAMPTZ NOT NULL,
                        ends_at TIMESTAMPTZ NOT NULL,
                        organiser_id INT REFERENCES users(id),
                        venue_id INT REFERENCES venues(id),
                        created_at TIMESTAMPTZ DEFAULT now()
                    );""")
        conn.commit()
    logger.info("Events table created")


def drop_events_table(conn: psycopg.connection):
    """create events table"""
    logger.info("DROPPING TABLE events")
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS events""")
        conn.commit()
    logger.info("Events table dropped")


def insert_events_data(conn: psycopg.connection,filepath):
    """execute to insert user data from .JSON file"""
    logging.info(f"inserting data from '{filepath}' into events")
    try:
        data = load_json_file(filepath)
        insert_statement = (
            """INSERT INTO events (title, description, starts_at, ends_at, organiser_id,venue_id)
            VALUES (%s, %s, %s,%s, %s, %s);"""
        )
        with conn.cursor() as curs:
            for row in data:
                curs.execute(
                    insert_statement, (row["title"], row["description"], row["starts_at"],row["ends_at"],row["organiser_id"],row["venue_id"])
                )
        conn.commit()
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")
    logging.info(f"data inserted into events")