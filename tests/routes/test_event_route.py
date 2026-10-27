import pytest

def test_get_events_returns_status_200(client ,cleanup):
    cleanup()
    response = client.get("/events")
    assert response.status_code == 200