from pydantic import BaseModel


class Venue(BaseModel):
    id: int
    name: str
    address: str
    capacity: int


class VenueList(BaseModel):
    venues: list[Venue]