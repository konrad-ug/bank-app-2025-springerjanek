import requests

URL = "http://localhost:5000"

def clear_registry():
    resp = requests.get(URL + "/api/accounts")
    for acc in resp.json():
        requests.delete(URL + f"/api/accounts/{acc['pesel']}")


def test_save_and_load_accounts_from_db():
    clear_registry()

    accounts = [
        {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901"},
        {"first_name": "Anna", "last_name": "Nowak", "pesel": "10987654321"},
    ]

    for acc in accounts:
        resp = requests.post(URL + "/api/accounts", json=acc)
        assert resp.status_code == 201

    resp = requests.post(URL + "/api/accounts/save")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Accounts saved"

    clear_registry()
    resp = requests.get(URL + "/api/accounts")
    assert resp.status_code == 200
    assert len(resp.json()) == 0

    resp = requests.post(URL + "/api/accounts/load")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Accounts loaded"

    resp = requests.get(URL + "/api/accounts")
    assert resp.status_code == 200
    loaded_accounts = resp.json()
    assert len(loaded_accounts) == 2

    loaded_pesels = {acc["pesel"] for acc in loaded_accounts}
    assert loaded_pesels == {"12345678901", "10987654321"}
