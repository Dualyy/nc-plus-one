import pytest
from conftest_routes import *

def test_post_api_auth_login_returns_status_200_when_successfull(client):
    response = client.post("/api/auth/login", json={'email': 'test.one@example.com', 'password': 'testpassword123'})
    assert response.status_code == 200

def test_post_api_auth_login_returns_status_400_when_not_given_valid_login(client):
    response = client.post("/api/auth/login")
    assert response.status_code == 400