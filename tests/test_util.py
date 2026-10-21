from src.util import *
import types
import pytest


# fixtures
@pytest.fixture  # JSON file reader
def json_user_file():
    return load_json_file("./db/data/users.json")


# TEST load_json
def test_load_json_file_is_invokeable():
    assert callable(load_json_file)


def test_load_json_file_returns_generator(json_user_file):

    # act
    result = json_user_file
    # assert
    assert isinstance(result, types.GeneratorType)


def test_load_json_file_returns_expected_values(json_user_file):
    # arrange
    expected = {
        "name": "Alice Rahman",
        "email": "alice@example.com",
        "password": "password123",
    }
    # act
    result = next(json_user_file)
    # assert
    assert result == expected


##########################################

# TEST create_user_table()


def test_create_user_table():
    assert callable(create_user_table)


# TEST insert_data


def test_insert_user_data_is_callable():
    assert callable(insert_user_data)


#TEST drop_user_table

def test_drop_user_table():
    assert callable(drop_user_table)