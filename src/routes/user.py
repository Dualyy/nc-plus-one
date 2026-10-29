from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
from src.rsvps_table_util import find_rsvp_of_user_for_event
from src.connection import get_connection
from psycopg.rows import dict_row
from fastapi import HTTPException
from src.security import get_current_user
from src.events_table_util import find_event_by_id
from src.models.user import TokenUser

user_router = APIRouter(prefix="/user")

@user_router.get("/user/me/events", status_code=200)
def get_event_attendees(event_id: int, user: TokenUser = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            return