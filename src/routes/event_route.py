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


event_router=APIRouter(prefix="/events")

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
    events:list[Event]

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

    return {"events": [Event(
                        id = int(event[0]),
                        title= event[1],
                        description= event[2],
                        starts_at= event[3],
                        ends_at= event[4],
                        organiser_id= int(event[5]),
                        venue_id= int(event[6])
    ) for event in events]}


@event_router.get("/{event_id}", response_model=EventDict)
def get_event_by_id(event_id: int):
    """Retrieve an event by id

    The endpoint queries main database to give precise info about an event
    
    PERMISSIONS: public
    """
    conn = get_connection()
    

    with conn.cursor(row_factory=dict_row) as crsr:
        crsr.execute("""SELECT e.*, v.name as venue_name, v.address as venue_address, v.capacity as capacity
                        FROM events e
                        INNER JOIN venues v
                        ON e.venue_id = v.id
                        WHERE e.id = %s
                        """,(event_id,))
        event = crsr.fetchall()
        conn.commit()
        conn.close()
    if list(event) == []:
        raise HTTPException(status_code=404,detail={"status_code": "404 NOT FOUND",
                                                     "msg": f"event id: {event_id} does not exist"})
    for e in event:
        return {
        "event": 
            Event(
                id=e["id"],
                title=e["title"],
                description=e["description"],
                starts_at=e["starts_at"],
                ends_at=e["ends_at"],
                location=e["venue_name"],
                address=e["venue_address"],
                capacity=e["capacity"],
                created_at=e["created_at"]
            )
    }


@event_router.post('/{event_id}/rsvp',dependencies=[Depends(get_current_user)], status_code= 201)
def create_RSVP(event_id: int, user: TokenUser = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:

            #TODO: refactor out => reusable
            event = find_event_by_id(crsr,event_id)
            if event is None:
                raise HTTPException(status_code=404,detail={"status_code": "404 NOT FOUND",
                                                     "msg": f"event id: {event_id} does not exist"})

            rsvp = find_rsvp_of_user_for_event(crsr,event_id ,user.id)
            if rsvp is None:
            
                crsr.execute("""
                            INSERT INTO rsvp(attendee_id,event_id)
                            VALUES (%s,%s)
                            RETURNING *""", (user.id,event_id))
                rsvp_event = crsr.fetchone()
                conn.commit()

                return RSVP(id=rsvp_event['id'],
                        attendee_id=rsvp_event['attendee_id'],
                        event_id=rsvp_event['event_id'],
                        created_at= rsvp_event['created_at'],)
            else:
                raise HTTPException(status_code=409,detail={"status_code": "409 CONFLICT",
                                                                     "msg": f"rsvp already exists for event: {event_id} for user {user.id}"})


@event_router.delete("/{event_id}/rsvp/me", status_code=204)
def delete_rsvp_for_event(event_id: int, user: TokenUser = Depends(get_current_user)):
    with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as crsr:
                event = find_event_by_id(crsr,event_id)
                if event is not None:
                    rsvp = find_rsvp_of_user_for_event(crsr,event_id ,user.id)
                    if rsvp is not None:
                        print(rsvp)
                        crsr.execute("""
                                    DELETE FROM rsvp
                                    WHERE event_id = %s AND attendee_id = %s;"""
                                    ,(event_id, user.id))
                        conn.commit()
                    else:
                        raise HTTPException(status_code=404,detail={"status_code": "404 NOTFOUND",
                                                                                                                 "msg": f"No rsvp exists for for user {user.id} at event {event_id} "})
                else: 
                    raise HTTPException(status_code=404,detail={"status_code": "404 NOTFOUND",
                                                                                         "msg": f"event {event_id} does not exist"
                    })

@event_router.post('/',dependencies=[Depends(get_current_user)], status_code= 201)
def create_event(event: CreateEvent, user: TokenUser = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as crsr:
            crsr.execute("""
                        INSERT INTO events (title,description,starts_at, ends_at, venue_id, organiser_id)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        RETURNING *""",(event.title, event.description, event.starts_at, event.ends_at, event.venue_id, user.id))
            conn.commit()
            created_event = crsr.fetchone()
    return created_event
