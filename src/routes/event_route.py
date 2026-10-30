from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
from src.table_utils.rsvps_table_util import find_rsvp_of_user_for_event
from src.connection import get_connection
from psycopg.rows import dict_row
from fastapi import HTTPException
from src.auth.security import get_current_user
from src.table_utils.events_table_util import find_event_by_id
from src.models.user import TokenUser

event_router = APIRouter(prefix="/events")


class Event(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    organiser_id: int | None = None
    venue_id: int | None = None
    location: str | None = None
    address: str | None = None
    capacity: int | None = None
    created_at: datetime | None = None


class EventList(BaseModel):
    events: list[Event]


class EventDict(BaseModel):
    event: Event


class EventID(BaseModel):
    id: int


class CreateRSVP(BaseModel):
    attendee_id: int
    event_id: int


class RSVP(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime


class CreateEvent(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int


class PatchEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    venue_id: Optional[int] = None


class Attendee(BaseModel):
    id: int
    name: str
    email: str
    rsvped_at: datetime

class ListAttendees(BaseModel):
    attendees: list[Attendee]


@event_router.get("/", response_model=EventList)
def get_events():
    """Retrieve a list of all events

    The endpoint queries main database to give an overview of all available events

    PERMISSIONS: public
    """
    conn = get_connection()

    with conn.cursor() as crsr:
        crsr.execute("""SELECT * FROM events
                        ORDER BY id""")
        events = crsr.fetchall()
        conn.commit()
        conn.close()

    return {
        "events": [
            Event(
                id=int(event[0]),
                title=event[1],
                description=event[2],
                starts_at=event[3],
                ends_at=event[4],
                organiser_id=int(event[5]),
                venue_id=int(event[6]),
            )
            for event in events
        ]
    }


@event_router.get("/{event_id}", response_model=EventDict)
def get_event_by_id(event_id: int):
    """Retrieve an event by id

    The endpoint queries main database to give precise info about an event

    PERMISSIONS: public
    """
    conn = get_connection()

    with conn.cursor(row_factory=dict_row) as crsr:
        crsr.execute(
            """SELECT e.*, v.name as venue_name, v.address as venue_address, v.capacity as capacity
                        FROM events e
                        INNER JOIN venues v
                        ON e.venue_id = v.id
                        WHERE e.id = %s
                        """,
            (event_id,),
        )
        event = crsr.fetchall()
        conn.commit()
        conn.close()
    if list(event) == []:
        raise HTTPException(
            status_code=404,
            detail={
                "status_code": "404 NOT FOUND",
                "msg": f"event id: {event_id} does not exist",
            },
        )
    for e in event:
        return {
            "event": Event(
                id=e["id"],
                title=e["title"],
                description=e["description"],
                starts_at=e["starts_at"],
                ends_at=e["ends_at"],
                location=e["venue_name"],
                address=e["venue_address"],
                capacity=e["capacity"],
                created_at=e["created_at"],
            )
        }


@event_router.post(
    "/{event_id}/rsvp", dependencies=[Depends(get_current_user)], status_code=201
)
def create_RSVP(event_id: int, user: TokenUser = Depends(get_current_user)) -> RSVP:
    """Create a RSVP for current user's to an event

    The endpoint creates a RSVP belonging to the current user for the given event.

    Returns 404 if the event does not exist or the user has no RSVP for it.
    Returns 409 if an RSVP already exists

    PERMISSIONS: authenticated user
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:

            event = find_event_by_id(crsr, event_id)
            if event is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status_code": "404 NOT FOUND",
                        "msg": f"event id: {event_id} does not exist",
                    },
                )

            rsvp = find_rsvp_of_user_for_event(crsr, event_id, user.id)
            if rsvp is None:

                crsr.execute(
                    """
                            INSERT INTO rsvp(attendee_id,event_id)
                            VALUES (%s,%s)
                            RETURNING *""",
                    (user.id, event_id),
                )
                rsvp_event = crsr.fetchone()
                conn.commit()

                return RSVP(
                    id=rsvp_event["id"],
                    attendee_id=rsvp_event["attendee_id"],
                    event_id=rsvp_event["event_id"],
                    created_at=rsvp_event["created_at"],
                )
            else:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "status_code": "409 CONFLICT",
                        "msg": f"rsvp already exists for event: {event_id} for user {user.id}",
                    },
                )


@event_router.delete("/{event_id}/rsvp/me", status_code=204)
def delete_rsvp_for_event(event_id: int, user: TokenUser = Depends(get_current_user)):
    """Delete the current user's RSVP for an event

    The endpoint removes the RSVP belonging to the current user for the given event.

    Returns 404 if the event does not exist or the user has no RSVP for it.

    PERMISSIONS: authenticated user (can only delete their own RSVP)

    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            event = find_event_by_id(crsr, event_id)
            if event is not None:
                rsvp = find_rsvp_of_user_for_event(crsr, event_id, user.id)
                if rsvp is not None:
                    print(rsvp)
                    crsr.execute(
                        """
                                    DELETE FROM rsvp
                                    WHERE event_id = %s AND attendee_id = %s;""",
                        (event_id, user.id),
                    )
                    conn.commit()
                else:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "status_code": "404 NOTFOUND",
                            "msg": f"No rsvp exists for for user {user.id} at event {event_id} ",
                        },
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status_code": "404 NOTFOUND",
                        "msg": f"event {event_id} does not exist",
                    },
                )


@event_router.post("/", dependencies=[Depends(get_current_user)], status_code=201)
def create_event(event: CreateEvent, user: TokenUser = Depends(get_current_user)):
    """Create a new event

    The endpoint inserts a new event into the main database and returns the created row.
    The authenticated user is assigned as organiser.


    PERMISSIONS: authenticated user

    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute(
                """
                        INSERT INTO events (title,description,starts_at, ends_at, venue_id, organiser_id)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        RETURNING *""",
                (
                    event.title,
                    event.description,
                    event.starts_at,
                    event.ends_at,
                    event.venue_id,
                    user.id,
                ),
            )
            conn.commit()
            created_event = crsr.fetchone()
    return created_event


@event_router.patch("/{event_id}", status_code=200)
def patch_event(
    event_id: int,
    event_updates: PatchEvent,
    user: TokenUser = Depends(get_current_user),
):
    """Update a event

    The endpoint updates a event in the main database and returns the updated row.
    Only the organiser can edit it.


    PERMISSIONS: authenticated user (only organiser can update an event)

    """
    ALLOWED_COLUMNS = {"title", "description", "starts_at", "ends_at", "venue_id"}
    updates = {}
    for key, value in event_updates:
        if key in ALLOWED_COLUMNS and value is not None:
            updates[key] = value

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            event = find_event_by_id(crsr, event_id)
            if event is None:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status_code": "404 NOT FOUND",
                        "msg": f"event with id {event_id} not found",
                    },
                )
            if event["organiser_id"] is not user.id:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status_code": "403 FORBIDDEN",
                        "msg": f"Insufficient rights",
                    },
                )
            else:
                if updates.get("starts_at", event["starts_at"]) >= updates.get(
                    "ends_at", event["ends_at"]
                ):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "status_code": "400 BAD REQUEST",
                            "msg": f"ends_at is before starts_at",
                        },
                    )
                set_string = ", ".join(
                    f"{event_key} = %s"
                    for event_key in updates.keys()
                    if event_key in ALLOWED_COLUMNS
                )
                crsr.execute(
                    f"""UPDATE events
                        SET {set_string}
                        WHERE id = %s
                        RETURNING *""",
                    (*updates.values(), event_id),
                )
                updated_event = crsr.fetchone()
                conn.commit()
                return updated_event


@event_router.get("/{event_id}/attendees", status_code=200)
def get_event_attendees(event_id: int, user: TokenUser = Depends(get_current_user)) -> ListAttendees:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            event = find_event_by_id(crsr, event_id)
            if event is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status_code": "404 NOT FOUND",
                        "msg": f"event id: {event_id} does not exist",
                    },
                )
            if event["organiser_id"] != user.id:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status_code": "403 FORBIDDEN",
                        "msg": f"user: {user.id} is not event organiser",
                    },
                )
            crsr.execute(
                """SELECT u.id, u.name, u.email, r.created_at AS rsvped_at
                            FROM rsvp r
                            INNER JOIN users u ON r.attendee_id = u.id
                            WHERE r.event_id = %s
                            ORDER BY r.created_at;
                            """,
                (event_id,),
            )
            list_attendees = crsr.fetchall()

    return ListAttendees(attendees=[attendee for attendee in list_attendees])