import pytest
from src.account import Account
from src.business_account import BusinessAccount
from lib.smtp import SMTPClient

@pytest.fixture
def account():
    acc = Account("Test", "Test", "12345678910")
    acc.historia = [100, -1, 500]
    return acc


@pytest.fixture
def business_account(mocker):
    mocker.patch(
        "src.business_account.BusinessAccount.check_nip_status",
        return_value=True
    )
    acc = BusinessAccount("DRUTEX", "1234567890")
    acc.historia = [5000, -1000, 500]
    return acc


def test_send_history_personal_account_success(account, mocker):
    send_mock = mocker.patch.object(
        SMTPClient,
        "send",
        return_value=True
    )

    result = account.send_history_via_email("test@example.com")

    assert result is True
    send_mock.assert_called_once()

    subject, text, email = send_mock.call_args[0]
    assert "Account Transfer History" in subject
    assert text == "Personal account history: [100, -1, 500]"
    assert email == "test@example.com"


def test_send_history_personal_account_failure(account, mocker):
    mocker.patch.object(SMTPClient, "send", return_value=False)

    assert account.send_history_via_email("fail@example.com") is False

def test_send_history_business_account_success(business_account, mocker):
    send_mock = mocker.patch.object(
        SMTPClient,
        "send",
        return_value=True
    )

    result = business_account.send_history_via_email("biz@example.com")

    assert result is True
    send_mock.assert_called_once()

    subject, text, email = send_mock.call_args[0]
    assert "Account Transfer History" in subject
    assert text == "Company account history: [5000, -1000, 500]"
    assert email == "biz@example.com"



def test_send_history_business_account_failure(business_account, mocker):
    mocker.patch.object(SMTPClient, "send", return_value=False)

    assert business_account.send_history_via_email("biz@example.com") is False