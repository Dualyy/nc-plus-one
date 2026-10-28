import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from src.connection import config
from src.user_table_util import get_user_by_id



JWT_SECRET = config.get("JWT_SECRET")
JWT_ALG = "HS256"

def create_JWT_token(id: int, name: str, admin: bool | None = False):
    return jwt.encode({"id": str(id),
                       "name": name,
                        "admin": admin,
                        "iat": datetime.now(timezone.utc),
                        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
                       }, JWT_SECRET, algorithm=JWT_ALG)

bearer_scheme = HTTPBearer()

def validate_token_expiration(timestamp: datetime):
    if timestamp > datetime.now():
        raise HTTPException(status_code=401,detail={"status_code": "401 UNAUTHORIZED",
                                                     "msg": f"Invalid Token"})

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    if credentials is None:
        raise
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        get_user_by_id(payload['id'])

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return payload

