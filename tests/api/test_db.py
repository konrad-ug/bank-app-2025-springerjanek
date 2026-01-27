import requests

URL = "http://localhost:5000"

def clear_registry():
    resp = requests.get(URL + "/api/accounts")
    for acc in resp.json():
        requests.delete(URL + f"/api/accounts/{acc['pesel']}")

def test_save_accounts_to_db():
    clear_registry()

    requests.post(URL + "/api/accounts", json={
        "first_name": "Jan",
        "last_name": "Kowalski",
        "pesel": "111",
    })

    requests.post(URL + "/api/accounts", json={
        "first_name": "Anna",
        "last_name": "Nowak",
        "pesel": "222",
    })

    response = requests.post(URL + "/api/accounts/save")

    assert response.status_code == 200
    assert response.json()["message"] == "Accounts saved"

def test_load_accounts_from_db():
    clear_registry()

    requests.post(URL + "/api/accounts", json={
        "first_name": "Jan",
        "last_name": "Kowalski",
        "pesel": "333",
    })

    requests.post(URL + "/api/accounts/save")

    requests.delete(URL + "/api/accounts/333")

    resp = requests.get(URL + "/api/accounts")
    assert len(resp.json()) == 0

    response = requests.post(URL + "/api/accounts/load")

    assert response.status_code == 200
    assert response.json()["message"] == "Accounts loaded"

    resp = requests.get(URL + "/api/accounts/333")
    assert resp.status_code == 200
    assert resp.json()["account"]["first_name"] == "Jan"
