import requests
import random

BASE_URL = "http://localhost:5000/api/accounts"

def test_create_and_delete_account_100_times():
    for i in range(100):
        pesel = f"12345{random.randint(10000,99999)}0"
        payload = { "first_name": "Test","last_name": "User", "pesel": pesel}

        resp = requests.post(BASE_URL, json=payload, timeout=0.5)

        assert resp.status_code == 201

        resp = requests.delete(f"{BASE_URL}/{pesel}", timeout=0.5)

        assert resp.status_code == 200
        assert resp.json()["message"] == "Account deleted"

def test_create_account_and_process_100_incoming_transactions():
    pesel = f"12345{random.randint(10000,99999)}0"
    payload = { "first_name": "Test","last_name": "User", "pesel": pesel}

    resp = requests.post(BASE_URL, json=payload, timeout=0.5)
    assert resp.status_code == 201

    expected_balance = 0

    for i in range(100):
        transfer_payload = {"amount": 10, "type": "incoming" }

        resp = requests.post(f"{BASE_URL}/{pesel}/transfer",json=transfer_payload,timeout=0.5)

        assert resp.status_code == 201
        expected_balance += 10

    resp = requests.get(f"{BASE_URL}/{pesel}", timeout=0.5)
    assert resp.status_code == 200

    data = resp.json()
    assert data["balance"] == expected_balance