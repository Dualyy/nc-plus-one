from src.util import load_json_file
import types
import pytest

@pytest.fixture
def json_user_file():
    return load_json_file('./db/data/users.json')



def test_load_json_file_is_invokeable():
    assert callable(load_json_file)


def test_load_json_file_returns_generator(json_user_file):
    #assert
    result = json_user_file

    assert isinstance(result,types.GeneratorType)

def test_load_json_file_returns_expected_values(json_user_file):
    result = next(json_user_file)
    expected = {
    "name": "Alice Rahman",
    "email": "alice@example.com",
    "password": "password123"
  }
    assert result == expected