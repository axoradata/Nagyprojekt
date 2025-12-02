# tests/test_main.py

def test_read_root(client):
    """
    Teszteljük a "/" végpontot.
    Várjuk a {"Hello": "Main World"} választ.
    """
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {"Hello": "Main World"}


def test_read_item(client):
    """
    Teszteljük a "/items/" végpontot paraméterekkel.
    A main.py-ban item_id (int) és q (str) szerepel.
    """
    response = client.get("/items/", params={"item_id": 10, "q": "teszt_uzenet"})

    assert response.status_code == 200

    data = response.json()
    assert data["item_id"] == 10
    assert data["q"] == "teszt_uzenet"