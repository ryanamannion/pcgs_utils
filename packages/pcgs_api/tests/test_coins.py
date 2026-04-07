"""Tests for coin-detail schema parsing using real API response fixtures."""

import pytest

from pcgs_api.schema.coin import (
    AuctionItem,
    AuctionListResponse,
    AuctionResponse,
    CoinFacts,
    CoinFactsImage,
    CoinImagesResponse,
    ImageDetail,
)


# ---------------------------------------------------------------------------
# Fixtures — verbatim responses captured from the PCGS Public API
# ---------------------------------------------------------------------------


@pytest.fixture
def coin_facts_by_grade_response() -> dict:
    """GetCoinFactsByGrade: PCGSNo=2986 (1977 1C RD), GradeNo=65."""
    return {
        "PCGSNo": "2986",
        "CertNo": "",
        "Name": "1977 1C, RD",
        "Year": 1977,
        "Denomination": "1C",
        "Mintage": "4469930000",
        "MintMark": "P",
        "MintLocation": "Philadelphia",
        "MetalContent": "95% Copper, 5% Zinc",
        "Diameter": 19.0,
        "Edge": "Plain",
        "Weight": 3.11,
        "Country": "The United States of America",
        "Grade": "MS65RD",
        "Designation": "RD",
        "PriceGuideValue": 18.0,
        "Population": 353,
        "PopHigher": 648,
        "CoinFactsLink": "www.pcgs.com/coinfacts/coin/detail/2986/65",
        "Designer": "Victor David Brenner/Frank Gasparro",
        "Images": [],
        "CoinFactsNotes": "<p>The 1977-P Lincoln Cent is very common.</p>",
        "MajorVariety": "",
        "MinorVariety": "",
        "DieVariety": "",
        "AuctionList": [],
        "SeriesName": "Lincoln Cents 1959 to Date",
        "Category": "Half-Cents and Cents",
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def coin_facts_by_cert_no_response() -> dict:
    """GetCoinFactsByCertNo: certNo=38109793, retrieveAllData=true.

    1966 25C SMS SP66 with images and TrueView.
    """
    return {
        "PCGSNo": "5998",
        "CertNo": "38109793",
        "Name": "1966 25C SMS",
        "Year": 1966,
        "Denomination": "25C",
        "Mintage": "2200000",
        "MintMark": "P",
        "MintLocation": "Philadelphia",
        "MetalContent": "75% Copper, 25% Nickel over a pure Copper center",
        "Diameter": 24.3,
        "Edge": "Reeded",
        "Weight": 5.67,
        "Country": "The United States of America",
        "Grade": "SP66",
        "Designation": "",
        "PriceGuideValue": 16.0,
        "Population": 1224,
        "PopHigher": 1662,
        "CoinFactsLink": "www.pcgs.com/coinfacts/coin/detail/5998/66",
        "Designer": "John Flanagan",
        "Images": [
            {
                "Thumbnail": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/small/175339377.jpg",
                "Fullsize": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/large/175339377.jpg",
            },
            {
                "Thumbnail": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/small/175339369.jpg",
                "Fullsize": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/large/175339369.jpg",
            },
        ],
        "CoinFactsNotes": None,
        "MajorVariety": "SMS",
        "MinorVariety": "",
        "DieVariety": "",
        "AuctionList": None,
        "SeriesName": "(None)",
        "Category": "Twenty Cents and Quarters",
        "HasTrueViewImage": True,
        "ImageReady": True,
        "IsNFCSecure": False,
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def coin_facts_no_data_response() -> dict:
    """GetCoinFactsByCertNo: cert not found (certNo=25252728 or 00000000)."""
    return {
        "IsValidRequest": True,
        "ServerMessage": "No data found",
    }


@pytest.fixture
def apr_by_cert_no_response() -> dict:
    """GetAPRByCertNo: certNo=49771606 (1934 5C MS65, Stack's Bowers 2024)."""
    return {
        "PCGSNo": "3972",
        "CertNo": "49771606",
        "Name": "1934 5C",
        "Grade": "MS65",
        "Year": "1934",
        "Denomination": "5C",
        "Auctions": [
            {
                "Service": "PCGS",
                "Date": "08-2024",
                "Auctioneer": "Stack's Bowers",
                "LotNo": 91114,
                "LotNumV2": "91114",
                "SaleName": "August 2024 Collectors Choice Online Auction - U.S. Coins",
                "CertNo": "49771606",
                "Price": 145.0,
                "IsCAC": False,
                "AuctionLotUrl": "https://auctions.stacksbowers.com/lots/view/3-1C0KZN",
            },
            {
                "Service": "PCGS",
                "Date": "05-2012",
                "Auctioneer": "Heritage Auctions",
                "LotNo": 7917,
                "LotNumV2": "7917",
                "SaleName": "2012 May 30- June 3 US Coins Signature Auction #1171",
                "CertNo": None,
                "Price": 207.0,
                "IsCAC": False,
                "AuctionLotUrl": "http://coins.ha.com/c/item.zx?saleNo=1171&lotNo=7917",
            },
        ],
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def apr_by_cert_no_no_data_response() -> dict:
    """GetAPRByCertNo: cert with no auction history."""
    return {
        "IsValidRequest": True,
        "ServerMessage": "No data found",
    }


@pytest.fixture
def apr_by_grade_response() -> dict:
    """GetAPRByGrade: PCGSNo=3972 (1934 5C), GradeNo=65, NumberOfRecords=2."""
    return {
        "PCGSNo": "3972",
        "Name": "1934 5C",
        "Year": "1934",
        "Denomination": "5C",
        "Auctions": [
            {
                "Service": "ICG",
                "Date": "03-2025",
                "Auctioneer": "Stack's Bowers",
                "LotNo": 97103,
                "LotNumV2": "97103",
                "SaleName": "March 2025 Collectors Choice Online Auction - U.S. Coins",
                "CertNo": "2611020701",
                "Price": 105.0,
                "IsCAC": False,
                "AuctionLotUrl": "https://auctions.stacksbowers.com/lots/view/3-1H686J",
            },
            {
                "Service": "PCGS",
                "Date": "08-2024",
                "Auctioneer": "Stack's Bowers",
                "LotNo": 91114,
                "LotNumV2": "91114",
                "SaleName": "August 2024 Collectors Choice Online Auction - U.S. Coins",
                "CertNo": "49771606",
                "Price": 145.0,
                "IsCAC": False,
                "AuctionLotUrl": "https://auctions.stacksbowers.com/lots/view/3-1C0KZN",
            },
        ],
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def apr_by_grade_invalid_response() -> dict:
    """GetAPRByGrade: invalid / unrecognised parameters."""
    return {
        "PCGSNo": None,
        "Name": None,
        "Year": None,
        "Denomination": None,
        "Auctions": None,
        "IsValidRequest": False,
        "ServerMessage": None,
    }


@pytest.fixture
def coin_images_response() -> dict:
    """GetImagesByCertNo: certNo=38109793 (1966 25C SMS, has TrueView)."""
    return {
        "CertNo": "38109793",
        "Images": [
            {
                "Url": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/175339377.jpg",
                "Resolution": "6000x3000",
                "Description": "Max",
            },
            {
                "Url": "https://d1htnxwo4o0jhw.cloudfront.net/pcgs/cert/38109793/175339371.jpg",
                "Resolution": "2905x2905",
                "Description": "Max Reverse (white background)",
            },
        ],
        "HasObverseImage": True,
        "HasReverseImage": True,
        "HasTrueViewImage": True,
        "ImageReady": True,
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def coin_images_no_data_response() -> dict:
    """GetImagesByCertNo: cert exists but has no images yet."""
    return {
        "CertNo": "25252728",
        "Images": [],
        "HasObverseImage": False,
        "HasReverseImage": False,
        "HasTrueViewImage": False,
        "ImageReady": False,
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


# ---------------------------------------------------------------------------
# CoinFacts schema tests
# ---------------------------------------------------------------------------


def test_parse_coin_facts_by_grade(coin_facts_by_grade_response):
    coin = CoinFacts(**coin_facts_by_grade_response)

    assert coin.is_valid_request is True
    assert coin.pcgs_no == "2986"
    assert coin.name == "1977 1C, RD"
    assert coin.year == 1977
    assert coin.denomination == "1C"
    assert coin.mint_mark == "P"
    assert coin.grade == "MS65RD"
    assert coin.price_guide_value == 18.0
    assert coin.population == 353
    assert coin.pop_higher == 648
    assert coin.images == []
    assert coin.auction_list == []
    # fields absent in GetCoinFactsByGrade response default to None
    assert coin.has_true_view_image is None
    assert coin.is_nfc_secure is None


def test_parse_coin_facts_by_cert_no(coin_facts_by_cert_no_response):
    coin = CoinFacts(**coin_facts_by_cert_no_response)

    assert coin.is_valid_request is True
    assert coin.cert_no == "38109793"
    assert coin.pcgs_no == "5998"
    assert coin.grade == "SP66"
    assert coin.has_true_view_image is True
    assert coin.image_ready is True
    assert coin.is_nfc_secure is False
    assert coin.auction_list is None  # no auctions in this fixture
    assert len(coin.images) == 2

    img = coin.images[0]
    assert isinstance(img, CoinFactsImage)
    assert img.thumbnail.endswith(".jpg")
    assert img.fullsize.endswith(".jpg")


def test_parse_coin_facts_no_data(coin_facts_no_data_response):
    coin = CoinFacts(**coin_facts_no_data_response)

    assert coin.is_valid_request is True
    assert coin.server_message == "No data found"
    assert coin.pcgs_no is None
    assert coin.cert_no is None


# ---------------------------------------------------------------------------
# AuctionResponse schema tests
# ---------------------------------------------------------------------------


def test_parse_apr_by_cert_no(apr_by_cert_no_response):
    resp = AuctionResponse(**apr_by_cert_no_response)

    assert resp.is_valid_request is True
    assert resp.pcgs_no == "3972"
    assert resp.cert_no == "49771606"
    assert resp.grade == "MS65"
    assert len(resp.auctions) == 2

    sale = resp.auctions[0]
    assert isinstance(sale, AuctionItem)
    assert sale.service == "PCGS"
    assert sale.price == 145.0
    assert sale.is_cac is False
    assert sale.cert_no == "49771606"

    # second record has null CertNo
    assert resp.auctions[1].cert_no is None


def test_parse_apr_by_cert_no_no_data(apr_by_cert_no_no_data_response):
    resp = AuctionResponse(**apr_by_cert_no_no_data_response)

    assert resp.is_valid_request is True
    assert resp.auctions is None
    assert resp.pcgs_no is None


# ---------------------------------------------------------------------------
# AuctionListResponse schema tests
# ---------------------------------------------------------------------------


def test_parse_apr_by_grade(apr_by_grade_response):
    resp = AuctionListResponse(**apr_by_grade_response)

    assert resp.is_valid_request is True
    assert resp.pcgs_no == "3972"
    assert resp.year == "1934"
    assert len(resp.auctions) == 2

    assert resp.auctions[0].auctioneer == "Stack's Bowers"
    assert resp.auctions[1].price == 145.0


def test_parse_apr_by_grade_invalid(apr_by_grade_invalid_response):
    resp = AuctionListResponse(**apr_by_grade_invalid_response)

    assert resp.is_valid_request is False
    assert resp.auctions is None
    assert resp.pcgs_no is None
    assert resp.server_message is None


# ---------------------------------------------------------------------------
# CoinImagesResponse schema tests
# ---------------------------------------------------------------------------


def test_parse_coin_images(coin_images_response):
    resp = CoinImagesResponse(**coin_images_response)

    assert resp.is_valid_request is True
    assert resp.cert_no == "38109793"
    assert resp.has_obverse_image is True
    assert resp.has_reverse_image is True
    assert resp.has_true_view_image is True
    assert resp.image_ready is True
    assert len(resp.images) == 2

    img = resp.images[0]
    assert isinstance(img, ImageDetail)
    assert img.resolution == "6000x3000"
    assert img.description == "Max"
    assert "cloudfront.net" in img.url


def test_parse_coin_images_empty(coin_images_no_data_response):
    resp = CoinImagesResponse(**coin_images_no_data_response)

    assert resp.is_valid_request is True
    assert resp.cert_no == "25252728"
    assert resp.images == []
    assert resp.has_obverse_image is False
    assert resp.has_true_view_image is False
    assert resp.image_ready is False
