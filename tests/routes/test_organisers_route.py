import pytest
from conftest_routes import *

def test_get_organiser_stats_returns_200_when_give_valid_organiser(client):
    response = client.get('organisers/1/stats')
    assert response.status_code == 200

def test_get_organiser_stats_returns_404_when_given_non_existent_organiser_(client):
    response = client.get('organisers/99/stats')
    assert response.status_code == 404