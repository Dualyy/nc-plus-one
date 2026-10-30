import pytest
from fastapi.testclient import TestClient
from main import app
from src.routes.auth_route import Token
from src.seed import seed
from src.connection import get_connection
from src.auth.security import *

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def cleanup():
    seed()

@pytest.fixture
def delete_events():
    conn = get_connection()
    with conn.cursor() as crsr:
        crsr.execute("""DELETE FROM rsvp""")
        crsr.execute("""DELETE FROM events""")
        conn.commit()
    conn.close()

@pytest.fixture
def login():
    return {"Authorization": f"Bearer {create_JWT_token(1,JWT_SECRET,JWT_ALG)}"}