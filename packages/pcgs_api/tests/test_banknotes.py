import pytest

from pcgs_api.schema.banknote import (
    BanknotesResponse, BanknoteResponse,
    BanknoteImagesResponse
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
    response_body = {
        "IsValidRequest": False,
        "ServerMessage": "Invalid CertNo"
    }
    return response_body


@pytest.fixture
def get_banknote_images_by_cert_no_bad_request_response():
    """Example from PCGS swagger docs if you just enter some random cert no e.g.
    https://api.pcgs.com/publicapi/banknotedetail/GetBanknoteImagesByCertNo?certNo=test
    """
    response_body = {
        "CertNo": "test",
        "Images": [],
        "HasObverseImage": False,
        "HasReverseImage": False,
        "HasTrueViewImage": False,
        "ImageReady": False,
        "IsValidRequest": True,
        "ServerMessage": "Request successful"
    }
    return response_body


def test_parse_get_banknote_by_grade_invalid(get_banknote_by_grade_invalid_response):
    resp_obj = BanknotesResponse(**get_banknote_by_grade_invalid_response)
    assert resp_obj.banknotes is None
    assert resp_obj.is_valid_request is True  # why ??
    assert len(resp_obj.server_message) > 0


def test_parse_get_banknote_by_cert_no_invalid(get_banknote_by_cert_no_invalid_response):
    resp_obj = BanknoteResponse(**get_banknote_by_cert_no_invalid_response)
    assert resp_obj.banknote is None
    assert resp_obj.is_valid_request is False
    assert len(resp_obj.server_message) > 0


def test_parse_get_banknote_images_by_cert_bad_request(get_banknote_images_by_cert_no_bad_request_response):
    resp_obj = BanknoteImagesResponse(**get_banknote_images_by_cert_no_bad_request_response)
    assert resp_obj.is_valid_request is True
    assert resp_obj.has_obverse_image is False
    assert resp_obj.has_reverse_image is False
    assert resp_obj.has_true_view_image is False
    assert resp_obj.image_ready is False
    assert resp_obj.images == []
    assert resp_obj.cert_no == "test"


if __name__ == "__main__":
    pytest.main()
