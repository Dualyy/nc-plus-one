from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from datetime import datetime
from src.connection import get_connection
from psycopg.rows import dict_row 
from fastapi import HTTPException
from src.security import get_current_user

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


@event_router.post('/{event_id}/rsvp',dependencies=[Depends(get_current_user)])
def create_RSVP():
    return "Hello"