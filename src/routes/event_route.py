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
from src.exceptions import *

event_router = APIRouter(prefix="/events")


class DetailedEvent(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime
    location: str
    address: str | None = None
    capacity: int | None = None
    created_at: datetime

class BasicEvent(BaseModel):
    id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None = None


class EventsList(BaseModel):
    events: list[BasicEvent]


class EventDict(BaseModel):
    event: DetailedEvent


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


@event_router.get("/")
def get_events() -> EventsList:
    """Retrieve a list of all events

    The endpoint queries main database to give an overview of all available events


    PERMISSIONS: public
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute("""SELECT * FROM events e
                            INNER JOIN venues v
                            ON e.venue_id = v.id
                            ORDER BY e.id""")
            events = crsr.fetchall()
            conn.commit()
        return EventsList(events=[
                BasicEvent(
                    id=int(event['id']),
                    title=event['title'],
                    description=event['description'],
                    starts_at=event['starts_at'],
                    ends_at=event['ends_at'],
                    location=event['address']
                )
                for event in events
            ])
        


@event_router.get("/{event_id}", response_model=EventDict)
def get_event_by_id(event_id: int):
    """Retrieve an event by id

    The endpoint queries main database to give precise info about an event and its venue

    throws 404 NOT FOUND when event_id does not exist

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
        raise event_not_found(event_id)
    for e in event:
        return EventDict(
            event= DetailedEvent(
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
        )


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
                raise event_not_found(event_id)

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
                raise conflict(f"rsvp for user: {user.id} already exists for event: {event_id} ")


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
                    raise not_found("rsvp",f"No rsvp found for user: {user.id} at event: {event_id}")
            else:
                raise event_not_found(event_id)


@event_router.post("/", dependencies=[Depends(get_current_user)], status_code=201)
def create_event(event: CreateEvent, user: TokenUser = Depends(get_current_user)):
    """Create a new event

    The endpoint inserts a new event into the main database and returns the created row.
    The authenticated user is assigned as organiser.
    required fields are: title, description, starts_at, ends_at, venue_id
    organiser id is taken from the currently logged in user.

    throws 400 BAD REQUEST if fields are missing

    PERMISSIONS: authenticated user

    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute(
                """
                        INSERT INTO events (title, description, starts_at, ends_at, venue_id, organiser_id)
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

    throws 404 if event not found
    throws 403 if a user who is not the organiser tries to update the event
    throws 400 if ends_at date is before starts_at

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
                raise event_not_found(event_id)
            if event["organiser_id"] is not user.id:
                raise forbidden()
            else:
                if updates.get("starts_at", event["starts_at"]) >= updates.get(
                    "ends_at", event["ends_at"]
                ):
                    raise bad_request(f"ends_at must be after starts_at")
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
    """Queries the main database to give a list of attendees for an organisers event.

        throws 403 if current user is not the event organiser
        throws 400 if event not found
    
        PERMISSION: authenticated user -> event organiser
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            event = find_event_by_id(crsr, event_id)
            if event is None:
                raise event_not_found()
            if event["organiser_id"] != user.id:
                raise forbidden(f"user: {user.id} is not event organiser")
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