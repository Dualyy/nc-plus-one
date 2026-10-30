from fastapi import APIRouter, Depends, FastAPI

from src.connection import get_connection
from psycopg.rows import dict_row
from fastapi import HTTPException

organisers_router = APIRouter(prefix="/organisers")


@organisers_router.get("/{organiser_id}/stats", status_code=200)
def get_organiser_stats_by_id(organiser_id: int):
    """The endpoint aggregates statistics for a given organiser
    and returns a JSON object

    It raises a 404 if organiser ID can not be found

    PERMISSION: public
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute("""
                            SELECT u.id, u.name, Count(e.id) as total_events, AVG(r.attendee_id) as avg_attendance,
                            MAX(r.attendee_id) as best_attendend_count
                            FROM users u
                            LEFT JOIN events e
                            ON u.id = e.organiser_id
                            LEFT JOIN rsvp r
                            ON e.id = r.event_id
                            GROUP BY u.id""")
            organiser = crsr.fetchone()
            if organiser is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status_code": "404 NOT FOUND",
                        "msg": f"organiser with id: {organiser_id} does not exist",
                    },
                )
