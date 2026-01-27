import pytest
from src.repositories.mongo_accounts_repository import MongoAccountsRepository
from src.account import Account

def test_load_all_uses_collection(mocker):
    repo = MongoAccountsRepository()
    mock_collection = mocker.Mock()

    repo._collection = mock_collection
    mock_collection.find.return_value = [
        {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "123",
            "balance": 100,
            "history": []
        }
    ]

    accounts = repo.load_all()

    assert len(accounts) == 1
    assert accounts[0].pesel == "123"

def test_save_all_clears_and_saves_accounts(mocker):
    repo = MongoAccountsRepository()
    mock_collection = mocker.Mock()
    repo._collection = mock_collection

    account1 = Account("Jan", "Kowalski", "123")
    account1.balance = 100

    account2 = Account("Anna", "Nowak", "456")
    account2.balance = 200

    accounts = [account1, account2]

    repo.save_all(accounts)

    mock_collection.delete_many.assert_called_once_with({})

    assert mock_collection.update_one.call_count == 2

    mock_collection.update_one.assert_any_call(
        {"pesel": "123"},
        {"$set": account1.to_dict()},
        upsert=True
    )

    mock_collection.update_one.assert_any_call(
        {"pesel": "456"},
        {"$set": account2.to_dict()},
        upsert=True
    )