import pytest

@pytest.fixture(autouse=True)
def mock_nip_status(mocker, request):
    if "no_nip_mock" in request.keywords:
        return
    mocker.patch("src.business_account.BusinessAccount.check_nip_status", return_value=True)
