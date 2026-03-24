import pytest
from unittest.mock import patch


def test_get_all_users_with_invalid_token(client):
    """
    Ez a teszt azt ellenőrzi, hogy a rendszer elutasítja-e a kérést,
    ha a token érvénytelen vagy nem létezik az adatbázisban.
    """

    with patch("moduls.token.Token.validator", return_value=False):
        response = client.get("/user/all", params={"token": "invalid_garbage_token"})

        data = response.json()

        assert response.status_code == 200
        assert data["status"] == 0
        assert data["message"] == "Nincs jogosultságod"