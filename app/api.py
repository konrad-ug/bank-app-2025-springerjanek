from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.account import Account
from src.repositories.mongo_accounts_repository import MongoAccountsRepository

repo = MongoAccountsRepository()

app = Flask(__name__)

registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    account = Account(data["first_name"], data["last_name"], data["pesel"])
    
    added = registry.add_account(account)
    if not added:
        return jsonify({"message": "PESEL already exists"}), 409

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
    
    account_data = {
        "first_name": updated.first_name,
        "last_name": updated.last_name,
        "pesel": updated.pesel,
        "balance": updated.balance
    }
    
    return jsonify({"message": "Account updated", "account": account_data}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    deleted = registry.delete_account(pesel)

    if not deleted:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({"message": "Account deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def account_transfer(pesel):
    acc = registry.search_account(pesel)
    if acc is None:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")

    if transfer_type not in ["incoming", "outgoing", "express"]:
        return jsonify({"message": "Invalid transfer type"}), 400

    success = False
    if transfer_type == "incoming":
        acc.add_balance(amount)
        success = True
    elif transfer_type == "outgoing":
        success = acc.make_a_transfer(amount)
    elif transfer_type == "express":
        success = acc.make_express_transfer(amount)

    if success:
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    else:
        return jsonify({"message": "Nieudana transakcja"}), 422
    
@app.route("/api/accounts/save", methods=["POST"])
def save_accounts():
    repo.save_all(registry.list_accounts())
    return jsonify({"message": "Accounts saved"}), 200


@app.route("/api/accounts/load", methods=["POST"])
def load_accounts():
    accounts = repo.load_all()
    registry.clear()
    for acc in accounts:
        registry.add_account(acc)
    return jsonify({"message": "Accounts loaded"}), 200