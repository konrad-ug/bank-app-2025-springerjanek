from behave import *
import requests

URL = "http://localhost:5000"

@given('I make an incoming transfer of {amount} to account with pesel "{pesel}"')
@when('I make an incoming transfer of {amount} to account with pesel "{pesel}"')
def incoming_transfer(context, amount, pesel):
    context.response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json={"amount": int(amount), "type": "incoming"}
    )

@when('I make an outgoing transfer of {amount} from account with pesel "{pesel}"')
def outgoing_transfer(context, amount, pesel):
    context.response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json={"amount": int(amount), "type": "outgoing"}
    )

@when('I make an express transfer of {amount} from account with pesel "{pesel}"')
def express_transfer(context, amount, pesel):
    context.response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json={"amount": int(amount), "type": "express"}
    )

@then('Account with pesel "{pesel}" has balance equal to {balance}')
def check_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()["account"]
    assert account["balance"] == int(balance)
