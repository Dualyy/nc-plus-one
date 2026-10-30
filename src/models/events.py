from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateEvent(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int


class BasicEvent(BaseModel):
    id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None = None


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


class PatchEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    venue_id: Optional[int] = None


class EventsList(BaseModel):
    events: list[BasicEvent]


class EventDict(BaseModel):
    event: DetailedEvent


class RSVP(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime


class Attendee(BaseModel):
    id: int
    name: str
    email: str
    rsvped_at: datetime


class ListAttendees(BaseModel):
    attendees: list[Attendee]
