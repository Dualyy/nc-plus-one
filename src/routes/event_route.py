from fastapi import APIRouter, FastAPI

event_router=APIRouter()

@event_router.get("/events")
def get_events():
    pass