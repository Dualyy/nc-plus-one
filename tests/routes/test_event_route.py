import pytest
from conftest_routes import *
from src.routes.event_route import Event

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
    assert response.json()['error']['status_code'] == "404 NOT FOUND"
    assert response.json()['error']['msg'] == "event id: 999 does not exist"

def test_get_events_by_id_returns_400_when_given_id_that_is_invalid(client):
    invalid_id = "abc"
    response = client.get(f"/events/{invalid_id}")
    assert response.status_code == 400
    assert response.json()['error']['status_code'] == "400 BAD REQUEST"
    assert response.json()['error']['msg'] == "Input should be a valid integer, unable to parse string as an integer"


#----------------------------------------------------
#/events/:id/rvsp

def test_get_event_RSVP_creation_return_status_201_when_successfull(client,login):
    response = client.post("/events/4/rsvp",headers=login)
    assert response.status_code == 201
    assert response.json()['id'] == 7
    assert response.json()['attendee_id'] == 1
    assert response.json()['event_id'] == 4

def test_get_event_RSVP_creation_return_status_401_when_unauthenticated(client):
    response = client.post("/events/1/rsvp")
    assert response.status_code == 401
    assert response.json()['error'] == 'Not authenticated'

def test_get_event_RSVP_creation_return_status_404_when_event_not_found(client,login):
    response = client.post("/events/99/rsvp",headers=login)
    assert response.status_code == 404
    assert response.json()['error']['msg'] == "event id: 99 does not exist"


#----------------------------------------------------
#/events/:id/rvsp/me

def test_delete_event_RSVP_return_status_204_when_successfull(client,login):
    response = client.delete("/events/1/rsvp/me",headers=login)
    assert response.status_code == 204

def test_delete_event_RSVP_return_status_401_when_unauthenticated(client):
    response = client.delete("/events/1/rsvp/me")
    assert response.status_code == 401
    assert response.json()['error'] == 'Not authenticated'


#=========================================================
#POST /events

def test_post_event_creation_return_status_201_when_successfull(client,login):
    response = client.post("/events",json={
  "title": "Summer Rooftop Social",
  "description": "An evening of networking and good vibes.",
  "starts_at": "2025-08-15T18:00:00Z",
  "ends_at": "2025-08-15T21:00:00Z",
  "venue_id": 2
}, headers=login)
    assert response.status_code == 201

def test_post_event_creation_return_status_401_when_unauthenticated(client):
    response = client.post("/events")
    assert response.status_code == 401
    assert response.json()['error'] == 'Not authenticated'


#=========================================================
#PATCH /events
def test_patch_event_return_status_400_when_authorized_but_no_body(client,login):
    response = client.patch("/events/1",headers=login)
    assert response.status_code == 400

def test_patch_event_return_status_200_when_authorized_and_valid_body(client,login):
    input ={"title": "TestChange", "description": "A testing success"}
    response = client.patch("/events/1",json=input,headers=login)
    result = client.get("/events/1")
    
    assert response.status_code == 200
    assert result.json()['event']['title'] == input['title']
    assert result.json()['event']['description'] == input['description']

def test_patch_event_return_status_401_when_unauthenticated(client,login):
    response = client.patch("/events/1")
    assert response.status_code == 401

def test_patch_event_return_status_403_when_authenticated_and_valid_body_but_not_authorized(client,login):
    input ={"title": "TestChange", "description": "A testing success"}
    response = client.patch("/events/3",json=input,headers=login)
    
    assert response.status_code == 403
  