import pytest
from conftest_routes import *


# test /auth/login
def test_post_api_auth_login_returns_status_200_when_successfull(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "test.one@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200


def test_post_api_auth_login_returns_status_400_when_not_given_valid_login(
    client: TestClient,
):
    response = client.post("/auth/login")
    assert response.status_code == 400


def test_post_api_auth_login_returns_status_400_when_only_given_one_login_field(
    client: TestClient,
):
    response = client.post("/auth/login")
    assert response.status_code == 400
    assert response.json()["error"]["msg"] == "Field required"


# --------------------------------------------------------------------

# test /auth/register


def test_post_api_auth_register_returns_400_when_missing_fields(client: TestClient):
    response = client.post("/auth/register")
    assert response.status_code == 400
    assert response.json()["error"]["msg"] == "Field required"


def test_post_api_auth_register_returns_409_when_email_already_exists(
    client: TestClient,
):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test Attendee One",
            "email": "test.one@example.com",
            "password": "testpassword123",
        },
    )
    assert response.status_code == 400
    assert (
        response.json()["error"]["msg"]
        == "A user with email test.one@example.com already exists"
    )


def test_post_api_auth_register_returns_201_when_successfull(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test Attendee Six",
            "email": "test.Six@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201
