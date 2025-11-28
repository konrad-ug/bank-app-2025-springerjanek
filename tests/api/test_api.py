import requests

BASE_URL = "http://localhost:5000/api/accounts"

def create_account_on_server(pesel="12345678901", first_name="Test", last_name="User"):
    payload = {"first_name": first_name, "last_name": last_name, "pesel": pesel}
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    return payload

def test_get_account_by_pesel():
    account = create_account_on_server()
    response = requests.get(f"{BASE_URL}/{account['pesel']}")
    assert response.status_code == 200
    data = response.json()
    assert data["account"]["pesel"] == account["pesel"]
    assert data["account"]["first_name"] == account["first_name"]

def test_get_account_not_found():
    response = requests.get(f"{BASE_URL}/00000000000")
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Account not found"

def test_update_account():
    account = create_account_on_server()
    new_data = {"first_name": "Updated", "last_name": "Name"}
    response = requests.patch(f"{BASE_URL}/{account['pesel']}", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Account updated"

    get_resp = requests.get(f"{BASE_URL}/{account['pesel']}")
    updated_acc = get_resp.json()["account"]
    assert updated_acc["first_name"] == "Updated"
    assert updated_acc["last_name"] == "Name"

def test_delete_account():
    account = create_account_on_server()
    response = requests.delete(f"{BASE_URL}/{account['pesel']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Account deleted"

    #get_resp = requests.get(f"{BASE_URL}/{account['pesel']}")
    #assert get_resp.status_code == 404
