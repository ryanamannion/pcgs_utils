import pytest

from pcgs_api.schema.banknote import (
    GetBanknoteByGradeResponse, GetBanknoteByCertNoResponse
)

@pytest.fixture
def get_banknote_by_grade_invalid_response() -> dict:
    """Example from PCGS swagger docs for Request URL:
    https://api.pcgs.com/publicapi/banknotedetail/GetBanknoteByGrade?pcgsNo=test&gradeNo=1
    """
    response_body = {
        "Banknotes": None,
        "IsValidRequest": True,  # not sure why this is True, tbh
        "ServerMessage": "No data found, PCGS No Or Grade No might be invalid!"
    }
    return response_body


@pytest.fixture
def get_banknote_by_cert_no_invalid_response() -> dict:
    """Example from PCGS swagger docs for Request URL:
    https://api.pcgs.com/publicapi/banknotedetail/GetBanknoteByCertNo?certNo=test
    """
    request_body = {
        "IsValidRequest": False,
        "ServerMessage": "Invalid CertNo"
    }
    return request_body


def test_parse_get_banknote_by_grade_invalid(get_banknote_by_grade_invalid_response):
    resp_obj = GetBanknoteByGradeResponse(**get_banknote_by_grade_invalid_response)
    assert resp_obj.banknotes is None
    assert resp_obj.is_valid_request is True  # why ??
    assert len(resp_obj.server_message) > 0


def test_parse_get_banknote_by_cert_no_invalid(get_banknote_by_cert_no_invalid_response):
    resp_obj = GetBanknoteByCertNoResponse(**get_banknote_by_cert_no_invalid_response)
    assert resp_obj.banknote is None
    assert resp_obj.is_valid_request is False
    assert len(resp_obj.server_message) > 0


if __name__ == "__main__":
    pytest.main()
