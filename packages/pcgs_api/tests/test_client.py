"""Tests for PCGSClient — rate limiting, call counting, and request routing.

HTTP calls are intercepted with httpx's built-in mock transport so no real
network requests are made.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from unittest.mock import patch

import httpx
import pytest
import pytest_asyncio

from pcgs_api.client import PCGSClient, RateLimitExceeded
from pcgs_api.schema.coin import AuctionListResponse, AuctionResponse, CoinFacts, CoinImagesResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FAKE_KEY = "test-api-key"


def _make_transport(responses: dict[str, dict]) -> httpx.MockTransport:
    """Build an httpx mock transport that returns canned JSON for each path.

    Args:
        responses: Mapping of URL path substring to the JSON body to return.
            The first matching key wins.

    Returns:
        An ``httpx.MockTransport`` instance.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        for key, body in responses.items():
            if key in path:
                return httpx.Response(200, json=body)
        return httpx.Response(404, json={"error": "not found"})

    return httpx.MockTransport(handler)


def _client_with(responses: dict[str, dict], daily_limit: int = 1_000) -> PCGSClient:
    """Return a PCGSClient wired to a mock transport.

    Args:
        responses: Passed straight to :func:`_make_transport`.
        daily_limit: Override the daily request cap.

    Returns:
        A configured :class:`~pcgs_api.client.PCGSClient`.
    """
    client = PCGSClient(api_key=_FAKE_KEY, daily_limit=daily_limit)
    client._http = httpx.AsyncClient(
        base_url=client._base_url,
        transport=_make_transport(responses),
        headers={"Authorization": f"Bearer {_FAKE_KEY}"},
    )
    return client


# ---------------------------------------------------------------------------
# Fixtures — minimal valid response bodies
# ---------------------------------------------------------------------------


@pytest.fixture
def coin_facts_body() -> dict:
    return {
        "PCGSNo": "2986",
        "CertNo": "38109793",
        "Name": "1977 1C, RD",
        "Year": 1977,
        "Denomination": "1C",
        "Grade": "MS65RD",
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def no_data_body() -> dict:
    return {"IsValidRequest": True, "ServerMessage": "No data found"}


@pytest.fixture
def apr_by_grade_body() -> dict:
    return {
        "PCGSNo": "3972",
        "Name": "1934 5C",
        "Year": "1934",
        "Denomination": "5C",
        "Auctions": [
            {
                "Service": "PCGS",
                "Date": "08-2024",
                "Auctioneer": "Stack's Bowers",
                "LotNo": 91114,
                "LotNumV2": "91114",
                "SaleName": "August 2024 CCO Auction",
                "CertNo": "49771606",
                "Price": 145.0,
                "IsCAC": False,
                "AuctionLotUrl": "https://auctions.stacksbowers.com/lots/view/3-1C0KZN",
            }
        ],
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


@pytest.fixture
def coin_images_body() -> dict:
    return {
        "CertNo": "38109793",
        "Images": [
            {
                "Url": "https://example.com/img.jpg",
                "Resolution": "6000x3000",
                "Description": "Max",
            }
        ],
        "HasObverseImage": True,
        "HasReverseImage": True,
        "HasTrueViewImage": True,
        "ImageReady": True,
        "IsValidRequest": True,
        "ServerMessage": "Request successful",
    }


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------


def test_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("PCGS_ACCESS_TOKEN", raising=False)
    with pytest.raises(ValueError, match="API key"):
        PCGSClient()


def test_accepts_env_var_key(monkeypatch):
    monkeypatch.setenv("PCGS_ACCESS_TOKEN", "env-key")
    client = PCGSClient()
    assert client.api_key == "env-key"


def test_explicit_key_takes_precedence(monkeypatch):
    monkeypatch.setenv("PCGS_ACCESS_TOKEN", "env-key")
    client = PCGSClient(api_key="explicit-key")
    assert client.api_key == "explicit-key"


def test_default_daily_limit():
    client = PCGSClient(api_key=_FAKE_KEY)
    assert client.daily_limit == 1_000


def test_custom_daily_limit():
    client = PCGSClient(api_key=_FAKE_KEY, daily_limit=5_000)
    assert client.daily_limit == 5_000


# ---------------------------------------------------------------------------
# Rate limiting and call counting
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_counts_increment(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body})

    assert client.calls_this_session == 0
    assert client.calls_today == 0

    await client.get_coin_facts_by_cert_no("38109793")
    assert client.calls_this_session == 1
    assert client.calls_today == 1

    await client.get_coin_facts_by_cert_no("38109793")
    assert client.calls_this_session == 2
    assert client.calls_today == 2

    await client.close()


@pytest.mark.asyncio
async def test_remaining_calls_decrements(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body}, daily_limit=10)

    assert client.remaining_calls_today == 10

    await client.get_coin_facts_by_cert_no("38109793")
    assert client.remaining_calls_today == 9

    await client.close()


@pytest.mark.asyncio
async def test_rate_limit_exceeded_raises(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body}, daily_limit=1)

    await client.get_coin_facts_by_cert_no("38109793")  # consumes the only call

    with pytest.raises(RateLimitExceeded):
        await client.get_coin_facts_by_cert_no("38109793")

    await client.close()


@pytest.mark.asyncio
async def test_rate_limit_error_message_contains_reset_date(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body}, daily_limit=1)
    await client.get_coin_facts_by_cert_no("38109793")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(RateLimitExceeded, match=tomorrow):
        await client.get_coin_facts_by_cert_no("38109793")

    await client.close()


@pytest.mark.asyncio
async def test_daily_count_resets_on_new_day(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body})

    await client.get_coin_facts_by_cert_no("38109793")
    assert client.calls_today == 1

    # Simulate the calendar rolling over to tomorrow.
    client._reset_date = date.today() - timedelta(days=1)
    assert client.calls_today == 0

    await client.close()


@pytest.mark.asyncio
async def test_session_count_survives_day_rollover(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body})

    await client.get_coin_facts_by_cert_no("38109793")
    client._reset_date = date.today() - timedelta(days=1)
    _ = client.calls_today  # triggers reset

    assert client.calls_this_session == 1  # session count is never reset

    await client.close()


# ---------------------------------------------------------------------------
# Context-manager lifecycle
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_context_manager_closes_http(coin_facts_body):
    client = PCGSClient(api_key=_FAKE_KEY)
    async with client:
        assert client._http is not None
    assert client._http is None


@pytest.mark.asyncio
async def test_explicit_close(coin_facts_body):
    client = _client_with({"/coindetail/GetCoinFactsByCertNo": coin_facts_body})
    await client.close()
    assert client._http is None


# ---------------------------------------------------------------------------
# Authorization header
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_bearer_token_sent(coin_facts_body):
    """Verify the Authorization header is included in every request."""
    captured: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json=coin_facts_body)

    client = PCGSClient(api_key=_FAKE_KEY)
    client._http = httpx.AsyncClient(
        base_url=client._base_url,
        transport=httpx.MockTransport(handler),
        headers={"Authorization": f"Bearer {_FAKE_KEY}"},
    )

    await client.get_coin_facts_by_cert_no("38109793")
    await client.close()

    assert len(captured) == 1
    assert captured[0].headers["Authorization"] == f"Bearer {_FAKE_KEY}"


# ---------------------------------------------------------------------------
# Coin detail endpoints — response parsing
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_coin_facts_by_cert_no(coin_facts_body):
    client = _client_with({"/GetCoinFactsByCertNo": coin_facts_body})
    result = await client.get_coin_facts_by_cert_no("38109793")
    await client.close()

    assert isinstance(result, CoinFacts)
    assert result.is_valid_request is True
    assert result.pcgs_no == "2986"
    assert result.name == "1977 1C, RD"


@pytest.mark.asyncio
async def test_get_coin_facts_by_grade(coin_facts_body):
    client = _client_with({"/GetCoinFactsByGrade": coin_facts_body})
    result = await client.get_coin_facts_by_grade("2986", 65)
    await client.close()

    assert isinstance(result, CoinFacts)
    assert result.is_valid_request is True


@pytest.mark.asyncio
async def test_get_coin_facts_by_barcode(no_data_body):
    client = _client_with({"/GetCoinFactsByBarcode": no_data_body})
    result = await client.get_coin_facts_by_barcode("000000000000", "PCGS")
    await client.close()

    assert isinstance(result, CoinFacts)
    assert result.server_message == "No data found"


@pytest.mark.asyncio
async def test_get_apr_by_cert_no(no_data_body):
    client = _client_with({"/GetAPRByCertNo": no_data_body})
    result = await client.get_apr_by_cert_no("25252728")
    await client.close()

    assert isinstance(result, AuctionResponse)
    assert result.is_valid_request is True


@pytest.mark.asyncio
async def test_get_apr_by_grade(apr_by_grade_body):
    client = _client_with({"/GetAPRByGrade": apr_by_grade_body})
    result = await client.get_apr_by_grade("3972", 65, number_of_records=1)
    await client.close()

    assert isinstance(result, AuctionListResponse)
    assert result.pcgs_no == "3972"
    assert len(result.auctions) == 1
    assert result.auctions[0].price == 145.0


@pytest.mark.asyncio
async def test_get_apr_by_barcode(apr_by_grade_body):
    client = _client_with({"/GetAPRByBarcode": apr_by_grade_body})
    result = await client.get_apr_by_barcode("000000000000", "PCGS")
    await client.close()

    assert isinstance(result, AuctionListResponse)


@pytest.mark.asyncio
async def test_get_coin_images_by_cert_no(coin_images_body):
    client = _client_with({"/GetImagesByCertNo": coin_images_body})
    result = await client.get_coin_images_by_cert_no("38109793")
    await client.close()

    assert isinstance(result, CoinImagesResponse)
    assert result.has_true_view_image is True
    assert len(result.images) == 1
    assert result.images[0].resolution == "6000x3000"
