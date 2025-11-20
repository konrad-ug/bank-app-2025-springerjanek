from src.account import BusinessAccount

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