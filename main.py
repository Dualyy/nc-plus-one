from src.seed import seed
from fastapi import FastAPI

from src.routes.event_route import event_router
from src.routes.auth_route import auth_router
from src.routes.user_route import user_router

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.security import *

app = FastAPI(title="nc_plus_one")
app.include_router(event_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def HTTP_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def HTTP_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(status_code=400,detail={"status_code": "400 BAD REQUEST",
                                                         "msg": exc.errors()[0]['msg'],
                                                         "field": exc.args[0][0]['loc']})



seed()