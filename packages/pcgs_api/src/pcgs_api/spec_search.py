"""SpecSearch client — unauthenticated AJAX search on collectorsuniverse.com.

This wraps the internal autocomplete/search endpoint used by the PCGS and PSA
coin/card lookup UI.  No API key is required; the server only checks for
browser-like headers.

Note: httpx is blocked by Cloudflare TLS fingerprinting on this host; the
client uses ``urllib`` which passes the fingerprint check.

Usage::

    client = SpecSearchClient()
    coins = client.search_pcgs("morgan", max_results=10)
    cards = client.search_psa("babe ruth", max_results=5)

The ``specno`` in each result maps to the PCGS specification number and can be
passed directly to :meth:`~pcgs_api.client.PCGSClient.get_coin_facts_by_grade`.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

__all__ = [
    "SpecSearchClient",
    "SearchType",
    "PCGSCoinResult",
    "PCGSWorldCoinResult",
    "PSACardResult",
]

_BASE_URL = "https://www.collectorsuniverse.com"
_SEARCH_PATH = "/SpecSearch/Search/{company}"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/javascript, application/javascript, "
        "application/ecmascript, */*; q=0.01"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.collectorsuniverse.com/",
    "X-Requested-With": "XMLHttpRequest",
}


class SearchType(str, Enum):
    """Match mode for the ``searchType`` query parameter.

    Controls how the search ``term`` is matched against coin or card
    descriptions in the SpecSearch index.
    """

    LAST_TERM_WILDCARD = "LastTermWildCard"
    """Wildcard is applied to the last word of ``term`` (default autocomplete behaviour)."""

    STARTS_WITH = "StartsWith"
    """Results must start with the full ``term`` string."""

    CONTAINS = "Contains"
    """Results must contain ``term`` anywhere in the description."""

    EXACT = "Exact"
    """Results must exactly match the ``term`` string."""


class PCGSCoinResult(BaseModel):
    """A single PCGS US coin result returned by :meth:`SpecSearchClient.search_pcgs`.

    The ``specno`` maps to the PCGS specification number and can be passed
    directly to :meth:`~pcgs_api.client.PCGSClient.get_coin_facts_by_grade`.
    """

    specno: str
    """PCGS specification (catalogue) number for this coin type."""

    description: str
    """Full descriptive name including year, denomination, and variety."""

    year: Optional[str] = None
    """Year of issue (may include mint mark, e.g. ``"1921-S"``)."""

    mintmark: Optional[str] = None
    """Date and mint mark as displayed in search results (e.g. ``"1921 S"``)."""

    category: Optional[str] = None
    """Full category path (e.g. ``"Dollars, Morgan Dollar"``)."""

    denomination: Optional[str] = None
    """Face value denomination (e.g. ``"$1"``, ``"25C"``)."""

    prefix: Optional[str] = None
    """Grade prefix indicating strike type (``"MS"`` = mint state, ``"PR"`` = proof)."""

    holder: Optional[str] = None
    """Variety or designation label shown on the PCGS holder."""

    countryname: Optional[str] = None
    """Country of issue (e.g. ``"The United States of America"``)."""

    ancestorcategoryid: Optional[str] = None
    """Comma-separated chain of ancestor category IDs for hierarchical filtering."""

    imageurl: Optional[str] = None
    """URL of the small preview image (``http://``)."""

    hoverimageurl: Optional[str] = None
    """URL of the hover/popup image (``http://``)."""

    score: Optional[str] = None
    """Relevance score assigned by the search engine (e.g. ``"569.18%"``)."""


class PCGSWorldCoinResult(BaseModel):
    """A single PCGS world coin result returned when ``world_only=True``.

    World coin results use a different field schema from US coins; notably
    they include catalogue reference numbers and lack image URLs.
    """

    specno: str
    """PCGS specification number for this world coin type."""

    description: str
    """Full descriptive name of the coin."""

    year: Optional[str] = None
    """Year of issue."""

    denomination: Optional[str] = None
    """Face value denomination in the issuing country's currency."""

    countryname: Optional[str] = None
    """Country of issue."""

    catalogno1: Optional[str] = None
    """Primary world coin catalogue reference number (e.g. Pick number for banknotes)."""

    catalogno2: Optional[str] = None
    """Secondary catalogue reference number."""

    currvariety: Optional[str] = None
    """Currency or variety description."""

    bankname: Optional[str] = None
    """Issuing bank or authority name."""

    score: Optional[str] = None
    """Relevance score assigned by the search engine."""


class PSACardResult(BaseModel):
    """A single PSA sports/trading card result returned by :meth:`SpecSearchClient.search_psa`."""

    specno: str
    """PSA specification number for this card."""

    description: str
    """Full descriptive name including year, set, and player/subject."""

    year: Optional[str] = None
    """Year or year range of the card set (e.g. ``"1952"``, ``"1909-11"``)."""

    sport: Optional[str] = None
    """Sport or collectible category (e.g. ``"BASEBALL CARDS"``)."""

    publisher: Optional[str] = None
    """Card set publisher or manufacturer (e.g. ``"TOPPS"``, ``"BOWMAN"``)."""

    cardnumber: Optional[str] = None
    """Card number within the set."""

    category: Optional[str] = None
    """Full category path (e.g. ``"Sport, BASEBALL CARDS, 1952, TOPPS"``)."""

    score: Optional[str] = None
    """Relevance score assigned by the search engine."""


class SpecSearchClient:
    """Unauthenticated client for the collectorsuniverse.com SpecSearch API.

    Args:
        base_url: Override the base URL (useful for testing).
        timeout: HTTP request timeout in seconds (default 15).
    """

    def __init__(
        self,
        base_url: str = _BASE_URL,
        timeout: float = 15.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, company: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        """Make a GET request using urllib.

        Note: httpx is blocked by Cloudflare TLS fingerprinting on this host;
        urllib passes because its TLS fingerprint is not flagged.
        """
        params.setdefault("_", int(time.time() * 1000))
        path = _SEARCH_PATH.format(company=company)
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v != ""})
        url = f"{self._base_url}{path}?{qs}"
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ------------------------------------------------------------------
    # Public search methods
    # ------------------------------------------------------------------

    def search_pcgs(
        self,
        term: str,
        *,
        search_type: SearchType = SearchType.LAST_TERM_WILDCARD,
        max_results: int = 25,
        ancestor_category_id: Optional[int] = None,
        include_world: bool = False,
        world_only: bool = False,
        priced_grades: bool = False,
        price_guide_only: bool = False,
        pop_only: bool = False,
        include_pop_only: bool = False,
        can_receive: bool = False,
        auction_price_only: bool = False,
        coin_facts_active: bool = False,
        pcgs_currency_only: bool = False,
        include_type_coins: bool = False,
    ) -> list[PCGSCoinResult] | list[PCGSWorldCoinResult]:
        """Search PCGS coin specifications.

        Args:
            term: Search term (e.g. ``"morgan"``, ``"1909 VDB"``).
            search_type: How to match ``term`` against coin descriptions.
            max_results: Maximum number of results to return (default 25).
            ancestor_category_id: Filter by PCGS category ID (e.g. ``2`` for
                Dollars).  Pass ``None`` to search all categories.
            include_world: Include world coins alongside US results.
            world_only: Return only world coins (changes the response schema
                to :class:`PCGSWorldCoinResult`).
            priced_grades: Limit to coins that have price guide grades.
            price_guide_only: Limit to price-guide coins only.
            pop_only: Limit to population-report coins only.
            include_pop_only: Include pop-only coins in results.
            can_receive: Limit to coins PCGS currently accepts for grading.
            auction_price_only: Limit to coins with auction price history.
            coin_facts_active: Limit to CoinFacts-linked entries.
            pcgs_currency_only: PCGS currency coins only.
            include_type_coins: Include type coins.

        Returns:
            A list of :class:`PCGSWorldCoinResult` when ``world_only=True``,
            otherwise a list of :class:`PCGSCoinResult`.
        """
        params: dict[str, Any] = {
            "term": term,
            "searchType": search_type.value,
            "maxresults": max_results,
            "includeTypeCoins": str(include_type_coins).lower(),
            "includeworld": str(include_world).lower(),
            "worldOnly": str(world_only).lower(),
            "ancestorCategoryId": ancestor_category_id or "",
            "pricedgrades": str(priced_grades).lower(),
            "priceguideonly": str(price_guide_only).lower(),
            "popOnly": str(pop_only).lower(),
            "includePopOnly": str(include_pop_only).lower(),
            "canReceive": str(can_receive).lower(),
            "auctionpriceonly": str(auction_price_only).lower(),
            "coinfactsActive": str(coin_facts_active).lower(),
            "pcgsCurrencyOnly": str(pcgs_currency_only).lower(),
        }

        data = self._get("PCGS", params)

        if world_only:
            return [PCGSWorldCoinResult(**row) for row in data]
        return [PCGSCoinResult(**row) for row in data]

    def search_psa(
        self,
        term: str,
        *,
        search_type: SearchType = SearchType.LAST_TERM_WILDCARD,
        max_results: int = 25,
    ) -> list[PSACardResult]:
        """Search PSA sports / trading card specifications.

        Args:
            term: Search term (e.g. ``"babe ruth"``, ``"1952 topps"``).
            search_type: How to match ``term`` against card descriptions.
            max_results: Maximum number of results to return (default 25).

        Returns:
            A list of :class:`PSACardResult`.
        """
        params: dict[str, Any] = {
            "term": term,
            "searchType": search_type.value,
            "maxresults": max_results,
        }

        data = self._get("PSA", params)
        return [PSACardResult(**row) for row in data]
