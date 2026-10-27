import pytest
from fastapi.testclient import TestClient
from main import app
from src.seed import seed

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def cleanup():
    seed()