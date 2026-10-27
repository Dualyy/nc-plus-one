import pytest
from conftest_routes import *

# /events
def test_get_events_returns_status_200(client):
    response = client.get("/events")
    assert response.status_code == 200

def test_get_events_returns_list_of_events(client):
    response = client.get("/events")
    assert isinstance(response.json()['events'],list)
    assert len(response.json()['events']) == 4

def test_get_events_returns_empty_list_when_no_events(client,delete_events):
    delete_events
    response = client.get("/events")
    assert len(response.json()['events']) == 0

#----------------------------------------------------
#/events/:id
def test_get_events_by_id_returns_status_200(client):
    response = client.get("/events/1")
    assert response.status_code == 200

def test_get_events_returns_event_with_given_id(client):
    response = client.get("/events/1")
    assert isinstance(response.json()['event'],dict)

def test_get_events_by_id_returns_404_when_given_id_that_doesnt_exist(client):
    invalid_id = 999
    response = client.get(f"/events/{invalid_id}")
    assert response.status_code == 404
    assert response.json()['error']['error'] == "404 NOT FOUND"
    assert response.json()['error']['msg'] == "event id: 999 does not exist"
