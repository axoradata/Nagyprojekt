import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from database import query

@pytest.fixture(autouse=True)
def skip_token_validation():
    """
    Kicseréljük a valódi Token.validator-t egy mockolt adatra,
    ami mindig True-t ad vissza.
    """
    with patch("moduls.token.Token.validator", return_value=True):
        yield

@pytest.fixture(scope="session")
def client():
    """
    Ez a fixture létrehozza a TestClient-et.
    A 'session' scope miatt csak egyszer indul el a tesztelés elején.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def db_cleanup():
    """
    Ez a fixture automatikusan lefut MINDEN teszt után.
    Kitakarítja a tesztelés alatt létrehozott júzereket.
    """
    yield

    try:
        query.insert_into("DELETE FROM users WHERE card_id LIKE 'TEST-%'")
        query.insert_into("DELETE FROM employee WHERE card_id LIKE 'TEST-%'")
    except Exception as e:
        print(f"Takarítási hiba: {e}")