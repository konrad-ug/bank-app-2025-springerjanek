import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
