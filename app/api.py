from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.account import Account

app = Flask(__name__)

registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = Account(data["first_name"], data["last_name"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.list_accounts()
    accounts_data = [{"first_name": acc.first_name, "last_name": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count=registry.accounts_number()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc=registry.search_account(pesel)
    if acc is not None:
        account_data = {
            "first_name": acc.first_name,
            "last_name": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance
        }
        return jsonify({"account": account_data}), 200
    else:
        return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    updated = registry.update_account(pesel, data)

    if updated is None:
        return jsonify({"message": "Account not found"}), 404
    
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    deleted = registry.delete_account(pesel)

    if not deleted:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({"message": "Account deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)