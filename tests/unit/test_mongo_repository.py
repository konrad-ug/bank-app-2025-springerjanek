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
            "pesel": "12345678901",
            "balance": 100,
            "history": []
        }
    ]

    accounts = repo.load_all()

    assert len(accounts) == 1
    assert accounts[0].pesel == "12345678901"

def test_save_all_clears_and_saves_accounts(mocker):
    repo = MongoAccountsRepository()
    mock_collection = mocker.Mock()
    repo._collection = mock_collection

    account1 = Account("Jan", "Kowalski", "12345678901")
    account1.balance = 100

    account2 = Account("Anna", "Nowak", "98765432109")
    account2.balance = 200

    repo.save_all([account1, account2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2

    mock_collection.update_one.assert_any_call(
        {"pesel": "12345678901"},
        {"$set": account1.to_dict()},
        upsert=True
    )

def test_init_with_collection_injected(mocker):
    mock_collection = mocker.Mock()

    repo = MongoAccountsRepository(collection=mock_collection)

    assert repo.collection == mock_collection
