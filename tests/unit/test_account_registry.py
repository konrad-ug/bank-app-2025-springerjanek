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
