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
            crsr.execute(
                """
                WITH event_counts AS (
                    SELECT e.id, e.organiser_id, COUNT(r.id) AS rsvp_count
                    FROM events e
                    LEFT JOIN rsvp r ON r.event_id = e.id
                    GROUP BY e.id, e.organiser_id
                ),
                organiser_stats AS (
                    SELECT
                        u.id   AS organiser_id,
                        u.name AS name,
                        COUNT(ec.id)                      AS total_events,
                        ROUND(AVG(ec.rsvp_count), 1)      AS avg_attendance,
                        MAX(ec.rsvp_count)                AS best_attended_count
                    FROM users u
                    JOIN event_counts ec ON ec.organiser_id = u.id
                    GROUP BY u.id, u.name
                ),
                ranked AS (
                    SELECT *, RANK() OVER (ORDER BY total_events DESC) AS organiser_rank
                    FROM organiser_stats
                )
                SELECT * FROM ranked WHERE organiser_id = %s;
                """,
                (organiser_id,),
            )
            organiser = crsr.fetchone()

    if organiser is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status_code": "404 NOT FOUND",
                "msg": f"organiser with id: {organiser_id} does not exist",
            },
        )

    organiser["avg_attendance"] = float(organiser["avg_attendance"])
    return {"stats": organiser}
