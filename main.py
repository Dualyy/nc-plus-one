from src.seed import seed
from fastapi import FastAPI
from src.routes.event_route import event_router

app = FastAPI(title="nc_plus_one")
app.include_router(event_router)

seed()