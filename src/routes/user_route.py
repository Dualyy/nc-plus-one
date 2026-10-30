from fastapi import APIRouter, Depends, FastAPI

from src.connection import get_connection
from psycopg.rows import dict_row
from src.auth.security import get_current_user

from src.models.user import TokenUser

user_router = APIRouter(prefix="/user")


@user_router.get("/me/events", status_code=200)
def get_event_attendees(user: TokenUser = Depends(get_current_user)):
    """Retrieve a list of all events the user has RSVPed to

    The endpoint queries main database to give an overview of all available events

    returns list of events with id, title, starts_at time, rsvp_date, the relative rank of it, and total amount of rsvps
    PERMISSIONS: public
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute(
                """
                            SELECT e.id, e.title, e.starts_at, r.created_at AS rsvp_date
                            FROM events e
                            INNER JOIN rsvp r
                            ON e.id = r.event_id
                            WHERE r.attendee_id = %s
                            ORDER BY e.starts_at, e.id
                            """,
                (user.id,),
            )
            rsvps = crsr.fetchall()
            rank = 0

            return {
                "events": [
                    {
                        "id": rsvp["id"],
                        "title": rsvp["title"],
                        "starts_at": rsvp["starts_at"],
                        "rsvp_date": rsvp["rsvp_date"],
                        "event_rank": rank,
                        "total_rsvps": len(rsvps),
                    }
                    for rank, rsvp in enumerate(rsvps, start=1)
                ]
            }
