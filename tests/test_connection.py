from src.connection import get_connection
import psycopg

def test_get_connection_returns_connection():
    assert isinstance(get_connection(),psycopg.Connection)