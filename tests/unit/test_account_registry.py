import pytest
from src.account import Account
from src.accounts_registry import AccountsRegistry

@pytest.fixture
def account():
    return Account("Jan", "Kowalski", "90010112345")

@pytest.fixture
def account2():
    return Account("Anna", "Nowak", "85010112345")

@pytest.fixture
def registry():
    return AccountsRegistry()

class TestAccountsRegistry:

    def test_add_account(self, registry, account):
        registry.add_account(account)
        assert registry.accounts_number() == 1
        assert registry.list_accounts()[0] == account

    def test_list_accounts(self, registry, account, account2):
        registry.add_account(account)
        registry.add_account(account2)
        result = registry.list_accounts()
        assert result == [account, account2]

    @pytest.mark.parametrize(
        "pesel, expected",
        [
            ("90010112345", True),
            ("11111111111", False),
        ]
    )
    def test_search_account(self, registry, account, pesel, expected):
        registry.add_account(account)
        found = registry.search_account(pesel)
        if expected:
            assert found is account
        else:
            assert found is None

    def test_accounts_number(self, registry, account, account2):
        assert registry.accounts_number() == 0
        registry.add_account(account)
        registry.add_account(account2)
        assert registry.accounts_number() == 2

    def test_update_account_success(self, registry, account):
        registry.add_account(account)

        updated = registry.update_account(
            "90010112345",
            {"first_name": "Janusz", "last_name": "Kowalski-Nowy"}
        )

        assert updated is account
        assert account.first_name == "Janusz"
        assert account.last_name == "Kowalski-Nowy"

    def test_update_account_partial_update(self, registry, account):
        registry.add_account(account)

        updated = registry.update_account(
            "90010112345",
            {"first_name": "Johny"}
        )

        assert updated is account
        assert account.first_name == "Johny"
        assert account.last_name == "Kowalski"

    def test_update_account_not_found(self, registry, account):
        registry.add_account(account)

        updated = registry.update_account("11111111111", {"first_name": "X"})
        assert updated is None

    def test_delete_account_success(self, registry, account, account2):
        registry.add_account(account)
        registry.add_account(account2)

        result = registry.delete_account("90010112345")

        assert result is True
        assert registry.accounts_number() == 1
        assert registry.search_account("90010112345") is None
        assert registry.list_accounts() == [account2]

    def test_delete_account_not_found(self, registry, account):
        registry.add_account(account)

        result = registry.delete_account("11111111111")

        assert result is False
        assert registry.accounts_number() == 1
