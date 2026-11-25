from fastapi import APIRouter

from src.connection import get_connection
from psycopg.rows import dict_row


venue_router = APIRouter(prefix="/venues")


@venue_router.get("", status_code=200)
def get_me():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute(
                            """
                            SELECT * FROM venues
                            """,
                (),
            )
            venues = crsr.fetchall()

            return {
                "venues": [
                    {
                       "id": venue["id"],
                       "name": venue["name"],
                       "address": venue["address"],
                       "capacity": venue["capacity"]
                    }
                    for venue in venues
                ]
            }
