import requests
import pytest
import random

BASE_URL = "http://localhost:5000/api/accounts"

@pytest.fixture
def create_account():
    pesel = f"12345{random.randint(10000,99999)}0"
    payload = {"first_name": "Test", "last_name": "User", "pesel": pesel}
    resp = requests.post(BASE_URL, json=payload)
    assert resp.status_code == 201
    yield payload
    # sprzątanie po teście
    requests.delete(f"{BASE_URL}/{pesel}")

def test_create_account_unique_pesel():
    payload = {"first_name": "John", "last_name": "Doe", "pesel": "12345678901"}
    
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Account created"
    
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 409
    assert response.json()["message"] == "PESEL already exists"

def test_get_account_by_pesel(create_account):
    response = requests.get(f"{BASE_URL}/{create_account['pesel']}")
    assert response.status_code == 200
    data = response.json()
    assert data["account"]["pesel"] == create_account["pesel"]
    assert data["account"]["first_name"] == create_account["first_name"]

def test_get_account_not_found():
    response = requests.get(f"{BASE_URL}/00000000000")
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Account not found"

def test_update_account(create_account):
    new_data = {"first_name": "Updated", "last_name": "Name"}
    response = requests.patch(f"{BASE_URL}/{create_account['pesel']}", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Account updated"

    get_resp = requests.get(f"{BASE_URL}/{data['account']['pesel']}")
    updated_acc = get_resp.json()["account"]

    assert updated_acc["first_name"] == "Updated"
    assert updated_acc["last_name"] == "Name"

def test_delete_account(create_account):
    response = requests.delete(f"{BASE_URL}/{create_account['pesel']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Account deleted"

def test_transfer_account_not_found():
    payload = {"amount": 100, "type": "incoming"}
    response = requests.post(f"{BASE_URL}/00000000000/transfer", json=payload)
    assert response.status_code == 404
    assert response.json()["message"] == "Account not found"

def test_transfer_incoming(create_account):
    payload = {"amount": 500, "type": "incoming"}
    resp = requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json=payload)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Zlecenie przyjęto do realizacji"

def test_transfer_outgoing_success(create_account):
    requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json={"amount": 500, "type": "incoming"})
    
    payload = {"amount": 200, "type": "outgoing"}
    resp = requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json=payload)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Zlecenie przyjęto do realizacji"

def test_transfer_outgoing_failure(create_account):
    payload = {"amount": 1000, "type": "outgoing"}
    resp = requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json=payload)
    assert resp.status_code == 422
    assert resp.json()["message"] == "Nieudana transakcja"

def test_transfer_express_success(create_account):
    requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json={"amount": 500, "type": "incoming"})
    
    payload = {"amount": 100, "type": "express"}
    resp = requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json=payload)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Zlecenie przyjęto do realizacji"

def test_transfer_invalid_type(create_account):
    payload = {"amount": 100, "type": "unknown"}
    resp = requests.post(f"{BASE_URL}/{create_account['pesel']}/transfer", json=payload)
    assert resp.status_code == 400
    assert resp.json()["message"] == "Invalid transfer type"

