import pytest
from src.account import Account
from src.business_account import BusinessAccount

@pytest.fixture
def account():
    return Account("Jan", "Kowalski", "90010112345")

@pytest.fixture
def business_account():
    return BusinessAccount("DRUTEX", "1234567890")

class TestLoanRegularAccount:
    @pytest.mark.parametrize(
        "history, amount, expected",
        [
            ([10, -5, 20, 30, 40], 100, True),
            ([10, 20, -5], 100, False), 
            ([10,10], 100, False)
        ]
    )
    def test_loan_last_three(self, account, history, amount, expected):
        account.historia = history
        assert account.submit_for_loan(amount) == expected

    @pytest.mark.parametrize(
        "history, amount, expected",
        [
            ([10, -2, 5, 20, 80], 100, True), 
            ([5, 5, 5, 5, -1], 100, False),   
            ([10, 10, 200, 200, -100], 30, True),      
        ]
    )
    def test_loan_last_five(self, account, history, amount, expected):
        account.historia = history
        assert account.submit_for_loan(amount) == expected


class TestLoanBusinessAccount:
    @pytest.mark.parametrize(
        "history, balance, amount, expected",
        [
            ([10, -5, -1775, 30, 40], 200, 100, True),
            ([-1775], 200, 100, True),
            ([-1775], 200, 101, False),
 
        ]
    )

    def test_loan_with_zus_transfer(self, business_account, history, balance, amount, expected):
        business_account.historia = history
        business_account.balance = balance
        assert business_account.take_loan(amount) == expected

    @pytest.mark.parametrize(
        "history, balance, amount, expected",
        [
            ([10, -5, 30, 40], 200, 100, False),
            ([], 200, 100, False),
            ([-5], 200, 101, False),
 
        ]
    )

    def test_loan_without_zus_transfer(self, business_account, history, balance, amount, expected):
        business_account.historia = history
        business_account.balance = balance
        assert business_account.take_loan(amount) == expected

