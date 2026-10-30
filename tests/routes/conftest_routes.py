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
    return {"Authorization": f"Bearer {create_JWT_token(1, JWT_SECRET, JWT_ALG)}"}


@pytest.fixture
def get_all_events():
    return client.get("/events")


@pytest.fixture
def test_event():
    return {
        "event": {
            "id": 1,
            "title": "[TEST] Alpha Meetup",
            "description": "Test fixture: standard evening event in BST.",
            "starts_at": "2026-06-11T18:30:00+01:00",
            "ends_at": "2026-06-11T21:00:00+01:00",
            "location": "[TEST] Venue One",
            "address": "1 Test Street, Testville, TE1 1ST",
            "capacity": 10,
            "created_at": "2026-10-30T13:51:12.001461Z",
        }
    }


@pytest.fixture
def test_list_of_attendees():
    return {
        "attendees": [
            {
                "id": 1,
                "name": "Test Attendee One",
                "email": "test.one@example.com",
                "rsvped_at": "2026-10-30T13:57:22.883697Z",
            }
        ]
    }
