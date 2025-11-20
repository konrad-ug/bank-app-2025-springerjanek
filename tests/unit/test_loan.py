from src.account import Account

class TestLoan:

    def test_loan_last_three_positive(self):
        acc = Account("Jan", "Kowalski", "90010112345")
        acc.historia = [10, -5, 20, 30, 40]

        result = acc.submit_for_loan(100)

        assert result is True
        assert acc.balance == 100

    def test_loan_last_three_not_all_positive(self):
        acc = Account("Jan", "Kowalski", "90010112345")
        acc.historia = [10, 20, -5]

        result = acc.submit_for_loan(100)

        assert result is False
        assert acc.balance == 0

    def test_loan_sum_last_five_greater(self):
        acc = Account("Jan", "Kowalski", "90010112345")
        acc.historia = [10, -2, 5, 20, 80]

        result = acc.submit_for_loan(100)

        assert result is True
        assert acc.balance == 100

    def test_loan_sum_last_five_not_greater(self):
        acc = Account("Jan", "Kowalski", "90010112345")
        acc.historia = [5, 5, 5, 5, -1]

        result = acc.submit_for_loan(100)

        assert result is False
        assert acc.balance == 0

    def test_loan_sum_last_five_greater_with_negative_transactions(self):
        acc = Account("Jan", "Kowalski", "90010112345")
        acc.historia = [10, 10, 200, 200, -100]

        result = acc.submit_for_loan(30)

        assert result is True
        assert acc.balance == 30
