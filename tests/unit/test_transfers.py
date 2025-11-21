import pytest
from src.account import Account
from src.business_account import BusinessAccount

@pytest.fixture
def personal_account():
    def _create(balance=0):
        acc = Account("John", "Doe", 12345678910)
        acc.add_balance(balance)
        return acc
    return _create

@pytest.fixture
def business_account():
    def _create(nip=1234567891, balance=0):
        acc = BusinessAccount("nazwa_firmy", nip)
        acc.add_balance(balance)
        return acc
    return _create

class TestRegularTransfer:

    @pytest.mark.parametrize(
        "account_type, nip, initial_balance, amount, expected_result, expected_balance",
        [
            ("personal", None, 100, 100, True, 0),
            ("personal", None, 0, 100, False, 0),
            ("personal", None, 100, -100, False, 100),
            ("personal", None, 50, 50, True, 0),
            ("personal", None, 0, -100, False, 0),
            ("business", 1234567891, 100, 100, True, 0),
            ("business", 231312, 100, 100, False, 100),
            ("business", 1234567891, 0, 100, False, 0),
            ("business", 1234567891, 100, -100, False, 100),
        ]
    )
    def test_make_a_transfer(self, personal_account, business_account, account_type, nip, initial_balance, amount, expected_result, expected_balance):
        if account_type == "personal":
            acc = personal_account(initial_balance)
        else:
            acc = business_account(nip, initial_balance)
        result = acc.make_a_transfer(amount)
        assert result == expected_result
        assert acc.balance == expected_balance

class TestExpressTransfer:

    @pytest.mark.parametrize(
        "account_type, nip, initial_balance, amount, expected_result, expected_balance",
        [
            ("personal", None, 100, 50, True, 49),
            ("personal", None, 0, 1, False, 0),
            ("personal", None, 1, 1, True, -1),
            ("business", 1234567891, 200, 100, True, 95),
            ("business", 1234567891, 5, 100, False, 5),
            ("business", 1234567891, 1, 1, True, -5),
        ]
    )
    def test_make_express_transfer(self, personal_account, business_account, account_type, nip, initial_balance, amount, expected_result, expected_balance):
        if account_type == "personal":
            acc = personal_account(initial_balance)
        else:
            acc = business_account(nip, initial_balance)
        result = acc.make_express_transfer(amount)
        assert result == expected_result
        assert acc.balance == expected_balance
