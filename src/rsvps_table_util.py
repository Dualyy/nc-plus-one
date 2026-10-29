from fastapi import HTTPException
import psycopg
import logging
from src.util import load_json_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def find_rsvp_of_user_for_event(crsr: psycopg.Cursor, event_id: int, user_id: int):
    crsr.execute(
        """
                        SELECT * FROM rsvp r
                        WHERE event_id = %s AND attendee_id = %s""",
        (event_id, user_id),
    )
    rsvp_event = crsr.fetchone()
    return rsvp_event


# TODO: fix doc strings
def create_rsvp_table(conn: psycopg.Connection):
    """create rsvp table"""
    logger.info("CREATE TABLE rsvp")
    with conn.cursor() as curs:
        curs.execute("""CREATE TABLE rsvp(
                        id SERIAL PRIMARY KEY,
                        attendee_id INT REFERENCES users(id),
                        event_id INT REFERENCES events(id),
                        created_at TIMESTAMPTZ DEFAULT now()
                    );""")
        conn.commit()
    logger.info("RSVP table created")


def drop_rsvp_table(conn: psycopg.Connection):
    """drop rsvp table"""
    logger.info("DROPPING TABLE rsvp")
    with conn.cursor() as curs:
        curs.execute("""DROP TABLE IF EXISTS rsvp""")
        conn.commit()
    logger.info("RSVP table dropped")


def insert_rsvp_data(conn: psycopg.Connection, filepath):
    """execute to insert rsvp data from .JSON file"""
    logging.info(f"inserting data from '{filepath}' into rsvp")
    try:
        data = load_json_file(filepath)
        insert_statement = "INSERT INTO rsvp (attendee_id, event_id) VALUES (%s, %s);"
        with conn.cursor() as curs:
            for row in data:
                curs.execute(insert_statement, (row["attendee_id"], row["event_id"]))
        conn.commit()
        logging.info(f"data inserted into rsvp")
    except (ConnectionError, psycopg.OperationalError, FileNotFoundError) as e:
        logging.error(f"Failed with: {e}")
