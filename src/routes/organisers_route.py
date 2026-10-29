from fastapi import APIRouter, Depends, FastAPI

from src.connection import get_connection
from psycopg.rows import dict_row
from fastapi import HTTPException
organisers_router=APIRouter(prefix="/organisers")




@organisers_router.get("/{organiser_id}/stats", status_code=200)
def get_organiser_stats_by_id(organiser_id: int):
    with get_connection() as conn:
         with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute("""
                            SELECT id, name
                            FROM users
                            WHERE id = %s""",(organiser_id,))
            organiser = crsr.fetchone()
            if organiser is None:
                raise HTTPException(
                                    status_code=404,
                                    detail={
                                        "status_code": "404 NOT FOUND",
                                        "msg": f"organiser with id: {organiser_id} does not exist",
                                    },
                                )
    pass