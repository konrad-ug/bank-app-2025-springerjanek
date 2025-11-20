import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe",12345678910)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == '12345678910'

    def test_account_creation_with_wrong_pesel(self):
        account = Account("John", "Doe",222)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "Invalid"

    def test_account_creation_with_wrong_pesel_and_promo(self):
        account = Account("John", "Doe",222,"PROM_XYZ")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "Invalid"
        assert account.balance == 0

    def test_account_creation_with_wrong_pesel_and_wrong_promo(self):
        account = Account("John", "Doe",222,"TESTTTT")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "Invalid"
        assert account.balance == 0
    
    def test_account_creation_with_no_promo(self):
        account = Account("John", "Doe",12345678910)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == '12345678910'
        assert account.balance == 0

    def test_account_creation_with_promo_before_1960(self):
        account = Account("Anna", "Kowalska", 44051401458, "PROM_ABC")
        assert account.balance == 0  # brak bonusu, bo urodzona przed 1960

    def test_account_creation_with_promo_after_1960(self):
        account = Account("Jan", "Nowak", '02270803628', "PROM_ABC")
        assert account.balance == 50
    
    def test_historia_operations(self):
        acc = Account("Jan", "Kowalski", 12345678910)
        acc.add_balance(500)
        assert acc.balance==500
        acc.make_express_transfer(300)
        assert acc.balance==199
        assert acc.historia == [500.0, -300.0, -1]
   
class TestPeselCenturies:
    def test_pesel_from_2100s(self):
        acc = Account("Adam", "Nowak", 21451401458)  # mm = 45
        assert acc.pesel == "21451401458"

    def test_pesel_from_2200s(self):
        acc = Account("Ewa", "Kowalska", 61651401458)  # mm = 65
        assert acc.pesel == "61651401458"