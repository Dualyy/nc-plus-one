from src.user_table_util import *
from src.venues_table_util import *
from src.connection import get_connection
from src.events_table_util import *
from src.rsvps_table_util import *

def seed():

    conn = get_connection()

    drop_rsvp_table(conn)
    drop_events_table(conn)
    drop_venues_table(conn)
    drop_user_table(conn)

    create_user_table(conn)
    insert_user_data(conn, "./db/data/users.json")

    create_venues_table(conn)
    insert_venues_data(conn, "./db/data/venues.json")

    create_events_table(conn)
    insert_events_data(conn,"./db/data/events.json")

    create_rsvp_table(conn)
    insert_rsvp_data(conn,"./db/data/rsvps.json")

