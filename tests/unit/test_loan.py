import pytest
from src.account import Account

@pytest.fixture
def account():
    return Account("Jan", "Kowalski", "90010112345")

class TestLoan:
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
