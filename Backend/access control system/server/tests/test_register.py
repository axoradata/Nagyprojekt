def test_admin_can_register_user(client):
    """
    Teszteljük a regisztrációt érvényes adatokkal.
    """
    params = {
        "card_id": "TEST-999",
        "disposition": "admin",
        "full_name": "Teszt Jakab",
        "password": "1234",
        "token": "EGY_TOKEN"
    }

    response = client.post("/user/register", params=params)

    assert response.status_code == 200
    assert response.json()["status"] == 1