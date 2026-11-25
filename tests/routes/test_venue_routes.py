import pytest
from conftest_routes import *


def test_get_venues(client):
    response = client.get("/venues")
    assert response.status_code == 200
    assert len(response.json()["venues"]) == 4
