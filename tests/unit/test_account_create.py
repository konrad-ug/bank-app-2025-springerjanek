import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.account import Account, BusinessAccount


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

class TestRegularTransfer:
    def test_make_a_transfer_with_available_funds(self):
        account = Account("John", "Doe",12345678910)
        account.add_balance(100)
        assert account.balance >= 100
        result = account.make_a_transfer(100)
        assert result is True
        assert account.balance == 0

    def test_make_a_transfer_without_available_funds(self):
        account = Account("John", "Doe",12345678910)
        result = account.make_a_transfer(100)
        assert result is False
        assert account.balance == 0

    def test_make_a_transfer_with_available_funds_and_wrong_amount(self):
        account = Account("John", "Doe",12345678910)
        account.add_balance(100)
        assert account.balance >= 100
        result = account.make_a_transfer(-100)
        assert result is False

    def test_make_transfer_exact_balance(self):
        acc = Account("John", "Doe", 12345678910)
        acc.add_balance(50)
        result = acc.make_a_transfer(50)
        assert result is True
        assert acc.balance == 0

    def test_make_a_transfer_without_available_funds_and_wrong_amount(self):
        account = Account("John", "Doe",12345678910)
        result = account.make_a_transfer(-100)
        assert result is False

    def test_make_a_transfer_with_available_funds_on_business_account(self):
        business_account = BusinessAccount("nazwa_firmy",1234567891)
        business_account.add_balance(100)
        assert business_account.balance >= 100
        result = business_account.make_a_transfer(100)
        assert result is True
        assert business_account.balance == 0

    def test_make_a_transfer_with_wrong_nip_and_available_funds(self):
        business_account = BusinessAccount("nazwa_firmy",231312)
        business_account.add_balance(100)
        assert business_account.balance >= 100
        result = business_account.make_a_transfer(100)
        assert result is False

    def test_make_a_transfer_without_available_funds_on_business_account(self):
        business_account = BusinessAccount("nazwa_firmy",1234567891)
        result = business_account.make_a_transfer(100)
        assert result is False
        assert business_account.balance == 0

    def test_make_a_transfer_with_available_funds_and_wrong_amount_on_business_account(self):
        business_account = BusinessAccount("nazwa_firmy",1234567891)
        business_account.add_balance(100)
        assert business_account.balance >= 100
        result = business_account.make_a_transfer(-100)
        assert result is False
    
class TestBusinessAcount:
    def test_make_valid_business_account(self):
        business_account = BusinessAccount("nazwa_firmy",1234567891)
        assert business_account.company_name == "nazwa_firmy"
        assert business_account.nip == '1234567891'
        assert business_account.balance == 0

    def test_make_valid_business_account_with_balance(self):
        business_account = BusinessAccount("nazwa_firmy",1234567891)
        business_account.add_balance(100)
        assert business_account.company_name == "nazwa_firmy"
        assert business_account.nip == '1234567891'
        assert business_account.balance == 100

    def test_make_invalid_business_account(self):
        business_account = BusinessAccount("nazwa_firmy",123456789123)
        assert business_account.company_name == "nazwa_firmy"
        assert business_account.nip == 'Invalid'  
        assert business_account.balance == 0


class TestExpressTransfer:
    def test_express_transfer_personal_account_with_funds(self):
        acc = Account("John", "Doe", 12345678910)
        acc.add_balance(100)
        result = acc.make_express_transfer(50)
        assert result is True
        assert acc.balance == 49

    def test_express_transfer_personal_account_without_enough_funds(self):
        acc = Account("John", "Doe", 12345678910)
        assert acc.make_express_transfer(1) is False
        assert acc.balance == 0

    def test_express_transfer_personal_account_at_limit(self):
        acc = Account("John", "Doe", 12345678910)
        acc.add_balance(1)
        result = acc.make_express_transfer(1)
        assert result is True
        assert acc.balance == -1

    def test_express_transfer_business_account_with_funds(self):
        acc = BusinessAccount("Firma", 1234567891)
        acc.add_balance(200)
        result = acc.make_express_transfer(100)
        assert result is True
        assert acc.balance == 95

    def test_express_transfer_business_account_without_enough_funds(self):
        acc = BusinessAccount("Firma", 1234567891)
        acc.add_balance(5)
        result = acc.make_express_transfer(100)
        assert result is False
        assert acc.balance == 5

    def test_express_transfer_business_account_can_go_negative(self):
        acc = BusinessAccount("Firma", 1234567891)
        acc.add_balance(1)
        result = acc.make_express_transfer(1)
        assert result is True
        assert acc.balance == -5
   
class TestPeselCenturies:
    def test_pesel_from_2100s(self):
        acc = Account("Adam", "Nowak", 21451401458)  # mm = 45
        assert acc.pesel == "21451401458"

    def test_pesel_from_2200s(self):
        acc = Account("Ewa", "Kowalska", 61651401458)  # mm = 65
        assert acc.pesel == "61651401458"