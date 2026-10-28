from src.user_table_util import *
from src.venues_table_util import *
from src.connection import get_connection, get_environment
from src.events_table_util import *
from src.rsvps_table_util import *
import os

def db_file_path():
    env = get_environment()
    if env == "test":
        return "./db/data_test/"
    if env == "development":
        return "./db/data/"
    raise ValueError(f"No seed data configured for ENV={env!r}")


def seed():

    conn = get_connection()
    print('-------------------------')
    drop_rsvp_table(conn)
    drop_events_table(conn)
    drop_venues_table(conn)
    drop_user_table(conn)
    print('-------------------------')
    create_user_table(conn)
    insert_user_data(conn, f"{db_file_path()}users.json")
    print('-------------------------')
    create_venues_table(conn)
    insert_venues_data(conn, f"{db_file_path()}venues.json")
    print('-------------------------')
    create_events_table(conn)
    insert_events_data(conn,f"{db_file_path()}events.json")
    print('-------------------------')
    create_rsvp_table(conn)
    insert_rsvp_data(conn,f"{db_file_path()}rsvps.json")

