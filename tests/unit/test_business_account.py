import pytest
from src.business_account import BusinessAccount

class TestBusinessAcount:
    def test_make_valid_business_account(self, mocker):
        mock_response = {"result": {"subject": {"statusVat": "Czynny"}}}
        mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response))

        business_account = BusinessAccount("nazwa_firmy",1234567891)
        assert business_account.company_name == "nazwa_firmy"
        assert business_account.nip == '1234567891'
        assert business_account.balance == 0

    def test_make_valid_business_account_with_balance(self,mocker):
        mock_response = {"result": {"subject": {"statusVat": "Czynny"}}}
        mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response))

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
    
    @pytest.mark.no_nip_mock
    def test_constructor_raises_when_company_not_registered(self, mocker):
        mock_response = {"result": {"subject": {"statusVat": "Nieczynny"}}}
        mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response))

        with pytest.raises(ValueError) as exc:
            BusinessAccount("nazwa_firmy", 1234567891)

        assert "Company not registered!!" == str(exc.value)