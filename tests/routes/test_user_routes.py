import pytest
from conftest_routes import *

# =========================================================
# GET user/me/events


def test_get_event_user_is_attending_when_authenticated(client, login):
    response = client.get("user/me/events", headers=login)
    assert response.status_code == 200
    assert len(response.json()["events"]) == 2


def test_get_event_user_is_attending_returns_401_when_unauthorized(client):
    response = client.get("user/me/events")
    assert response.status_code == 401
