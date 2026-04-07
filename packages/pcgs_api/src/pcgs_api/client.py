"""PCGS Public API client — sync and async.

Sync usage (default, no ``async``/``await`` required):

    client = PCGSClient()
    result = client.get_coin_facts_by_cert_no("12345678")
    print(client.calls_this_session)

Async usage (for async codebases):

    async with PCGSClient() as client:
        result = await client.get_coin_facts_by_cert_no_async("12345678")
        print(client.calls_this_session)

Every method is available in both forms.  The plain name is always the
blocking sync version; append ``_async`` for the awaitable coroutine.  Both
share the same rate-limit counters and daily-call tracking.

The API key is read from the ``PCGS_ACCESS_TOKEN`` environment variable by
default, or passed explicitly as ``api_key``.  Free-tier accounts are limited
to 1,000 requests per day; the client raises :exc:`RateLimitExceeded` before
making a call that would exceed the configured limit.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import os
from datetime import date, timedelta
from typing import Any, Optional

import httpx

from pcgs_api.schema.banknote import (
    BanknoteImagesResponse,
    BanknoteResponse,
    BanknotesResponse,
)
from pcgs_api.schema.coin import (
    AuctionListResponse,
    AuctionResponse,
    CoinFacts,
    CoinImagesResponse,
)
from pcgs_api.schema.order import OrdersResponse

__all__ = ["PCGSClient", "RateLimitExceeded"]

_BASE_URL = "https://api.pcgs.com/publicapi"
_FREE_TIER_DAILY_LIMIT = 1_000


class RateLimitExceeded(Exception):
    """Raised when the daily API call limit would be exceeded."""


def _with_sync_methods(cls: type) -> type:
    """Class decorator that generates a plain-name blocking wrapper for every
    public ``*_async`` coroutine method defined directly on the class.

    For example, ``get_coin_facts_by_cert_no_async`` produces
    ``get_coin_facts_by_cert_no``.  The wrapper is created with
    :func:`functools.wraps` so it inherits the name, docstring, and
    annotations of the async original.
    """
    for name, method in list(vars(cls).items()):
        if not name.endswith("_async") or not inspect.iscoroutinefunction(method):
            continue

        sync_name = name[: -len("_async")]

        def make_sync(async_fn: Any) -> Any:
            @functools.wraps(async_fn)
            def sync_wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
                return asyncio.run(async_fn(self, *args, **kwargs))
            return sync_wrapper

        setattr(cls, sync_name, make_sync(method))

    return cls


@_with_sync_methods
class PCGSClient:
    """PCGS Public API client with sync and async interfaces.

    Plain method names (e.g. ``get_coin_facts_by_cert_no``) are blocking and
    safe to call from ordinary Python code.  Append ``_async`` to get the
    awaitable coroutine version (e.g. ``get_coin_facts_by_cert_no_async``).

    Args:
        api_key: PCGS API key. Falls back to the ``PCGS_ACCESS_TOKEN``
            environment variable when omitted.
        daily_limit: Maximum requests allowed per calendar day. Defaults to
            1,000 (the free-tier limit). Increase for commercial licences.
        base_url: Override the API base URL (useful for testing).

    Raises:
        ValueError: If no API key is provided and ``PCGS_ACCESS_TOKEN`` is
            not set.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        daily_limit: int = _FREE_TIER_DAILY_LIMIT,
        base_url: str = _BASE_URL,
    ) -> None:
        self.api_key = api_key or os.environ.get("PCGS_ACCESS_TOKEN")
        if not self.api_key:
            raise ValueError(
                "An API key is required. Pass api_key= or set the "
                "PCGS_ACCESS_TOKEN environment variable."
            )
        self._daily_limit = daily_limit
        self._base_url = base_url.rstrip("/")

        self._session_count: int = 0
        self._daily_count: int = 0
        self._reset_date: date = date.today()

        # Set by __aenter__ to reuse the connection pool across async calls.
        # When None, _get() opens a one-shot client per request (sync path).
        self._http: Optional[httpx.AsyncClient] = None

    # ------------------------------------------------------------------
    # Async context-manager support
    # ------------------------------------------------------------------

    async def __aenter__(self) -> PCGSClient:
        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    # ------------------------------------------------------------------
    # Call-count / rate-limit properties
    # ------------------------------------------------------------------

    @property
    def calls_this_session(self) -> int:
        """Total API calls made since this client was instantiated."""
        return self._session_count

    @property
    def calls_today(self) -> int:
        """API calls attributed to today (resets at midnight local time)."""
        self._maybe_reset_daily_count()
        return self._daily_count

    @property
    def remaining_calls_today(self) -> int:
        """Calls remaining before the daily limit is reached."""
        return max(0, self._daily_limit - self.calls_today)

    @property
    def daily_limit(self) -> int:
        """Configured daily request limit."""
        return self._daily_limit

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _maybe_reset_daily_count(self) -> None:
        today = date.today()
        if today > self._reset_date:
            self._daily_count = 0
            self._reset_date = today

    def _default_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make an authenticated GET request, enforcing the rate limit.

        When ``self._http`` is set (async context manager), the existing
        connection pool is reused.  Otherwise a one-shot client is opened and
        closed for the single request, keeping each ``asyncio.run()`` call
        self-contained.
        """
        self._maybe_reset_daily_count()
        if self._daily_count >= self._daily_limit:
            reset_day = self._reset_date + timedelta(days=1)
            raise RateLimitExceeded(
                f"Daily API limit of {self._daily_limit} requests reached. "
                f"Resets on {reset_day}."
            )

        if self._http is not None:
            response = await self._http.get(path, params=params or {})
        else:
            async with httpx.AsyncClient(
                base_url=self._base_url,
                headers=self._default_headers(),
            ) as http:
                response = await http.get(path, params=params or {})

        response.raise_for_status()
        self._daily_count += 1
        self._session_count += 1
        return response.json()

    # ------------------------------------------------------------------
    # Coin detail endpoints
    # ------------------------------------------------------------------

    async def get_coin_facts_by_cert_no_async(
        self,
        cert_no: str,
        retrieve_all_data: bool = False,
    ) -> CoinFacts:
        """Look up a certified coin by its 7–8 digit certificate number.

        Args:
            cert_no: The certificate number printed on the PCGS holder.
            retrieve_all_data: When ``True``, the response also includes
                images, auction prices realized, and population data.

        Returns:
            A :class:`~pcgs_api.schema.coin.CoinFacts` instance.
        """
        data = await self._get(
            f"/coindetail/GetCoinFactsByCertNo/{cert_no}",
            {"retrieveAllData": str(retrieve_all_data).lower()},
        )
        return CoinFacts(**data)

    async def get_coin_facts_by_barcode_async(
        self,
        barcode: str,
        grading_service: str,
    ) -> CoinFacts:
        """Look up a coin using the barcode printed on the holder.

        Args:
            barcode: The barcode value from the PCGS or NGC holder.
            grading_service: Either ``"PCGS"`` or ``"NGC"``.

        Returns:
            A :class:`~pcgs_api.schema.coin.CoinFacts` instance.
        """
        data = await self._get(
            "/coindetail/GetCoinFactsByBarcode",
            {"barcode": barcode, "gradingService": grading_service},
        )
        return CoinFacts(**data)

    async def get_coin_facts_by_grade_async(
        self,
        pcgs_no: str,
        grade_no: int,
        plus_grade: bool = False,
    ) -> CoinFacts:
        """Look up coin facts by PCGS specification number and grade.

        Note:
            This endpoint does **not** return auction prices or price guide
            values. Use :meth:`get_coin_facts_by_cert_no_async` with
            ``retrieve_all_data=True`` for pricing data.

        Args:
            pcgs_no: The PCGS catalogue/specification number (not a cert no).
            grade_no: Numeric grade (e.g. ``65`` for MS-65).
            plus_grade: ``True`` if the grade includes a plus modifier.

        Returns:
            A :class:`~pcgs_api.schema.coin.CoinFacts` instance.
        """
        data = await self._get(
            "/coindetail/GetCoinFactsByGrade",
            {
                "PCGSNo": pcgs_no,
                "GradeNo": grade_no,
                "PlusGrade": str(plus_grade).lower(),
            },
        )
        return CoinFacts(**data)

    async def get_apr_by_cert_no_async(self, cert_no: str) -> AuctionResponse:
        """Fetch auction prices realized for a specific certified coin.

        Args:
            cert_no: Certificate number of the coin.

        Returns:
            An :class:`~pcgs_api.schema.coin.AuctionResponse` instance.
        """
        data = await self._get(f"/coindetail/GetAPRByCertNo/{cert_no}")
        return AuctionResponse(**data)

    async def get_apr_by_grade_async(
        self,
        pcgs_no: str,
        grade_no: int,
        plus_grade: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        number_of_records: int = 100,
    ) -> AuctionListResponse:
        """Fetch auction prices realized for a coin type at a given grade.

        Args:
            pcgs_no: PCGS specification number.
            grade_no: Numeric grade.
            plus_grade: ``True`` for plus-grade variants.
            start_date: Filter by auction date — ``mm-dd-yyyy`` format.
            end_date: Filter by auction date — ``mm-dd-yyyy`` format.
            number_of_records: Maximum number of auction records to return.

        Returns:
            An :class:`~pcgs_api.schema.coin.AuctionListResponse` instance.
        """
        params: dict[str, Any] = {
            "PCGSNo": pcgs_no,
            "GradeNo": grade_no,
            "PlusGrade": str(plus_grade).lower(),
            "NumberOfRecords": number_of_records,
        }
        if start_date is not None:
            params["StartDate"] = start_date
        if end_date is not None:
            params["EndDate"] = end_date

        data = await self._get("/coindetail/GetAPRByGrade", params)
        return AuctionListResponse(**data)

    async def get_apr_by_barcode_async(
        self,
        barcode: str,
        grading_service: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> AuctionListResponse:
        """Fetch auction prices realized using a holder barcode.

        Args:
            barcode: Barcode from the PCGS or NGC holder.
            grading_service: ``"PCGS"`` or ``"NGC"``.
            start_date: Filter by auction date — ``mm-dd-yyyy`` format.
            end_date: Filter by auction date — ``mm-dd-yyyy`` format.

        Returns:
            An :class:`~pcgs_api.schema.coin.AuctionListResponse` instance.
        """
        params: dict[str, Any] = {
            "barcode": barcode,
            "gradingService": grading_service,
        }
        if start_date is not None:
            params["StartDate"] = start_date
        if end_date is not None:
            params["EndDate"] = end_date

        data = await self._get("/coindetail/GetAPRByBarcode", params)
        return AuctionListResponse(**data)

    async def get_coin_images_by_cert_no_async(self, cert_no: str) -> CoinImagesResponse:
        """Fetch all available images for a certified coin.

        Args:
            cert_no: Certificate number of the coin.

        Returns:
            A :class:`~pcgs_api.schema.coin.CoinImagesResponse` instance.
        """
        data = await self._get(
            "/coindetail/GetImagesByCertNo",
            {"certNo": cert_no},
        )
        return CoinImagesResponse(**data)

    # ------------------------------------------------------------------
    # Banknote detail endpoints
    # ------------------------------------------------------------------

    async def get_banknote_by_cert_no_async(
        self,
        cert_no: str,
        language_code: Optional[str] = None,
    ) -> BanknoteResponse:
        """Fetch banknote certification details by certificate number.

        Args:
            cert_no: Banknote certificate number.
            language_code: Optional language code for localised descriptions.

        Returns:
            A :class:`~pcgs_api.schema.banknote.BanknoteResponse` instance.
        """
        params: dict[str, Any] = {"certNo": cert_no}
        if language_code is not None:
            params["languageCode"] = language_code

        data = await self._get("/banknotedetail/GetBanknoteByCertNo", params)
        return BanknoteResponse(**data)

    async def get_banknote_by_grade_async(
        self,
        pcgs_no: str,
        grade_no: int,
    ) -> BanknotesResponse:
        """Fetch banknote records by PCGS specification number and grade.

        Args:
            pcgs_no: PCGS banknote specification number.
            grade_no: Numeric grade.

        Returns:
            A :class:`~pcgs_api.schema.banknote.BanknotesResponse` instance.
        """
        data = await self._get(
            "/banknotedetail/GetBanknoteByGrade",
            {"pcgsNo": pcgs_no, "gradeNo": grade_no},
        )
        return BanknotesResponse(**data)

    async def get_banknote_images_by_cert_no_async(
        self,
        cert_no: str,
    ) -> BanknoteImagesResponse:
        """Fetch images for a certified banknote.

        Args:
            cert_no: Banknote certificate number.

        Returns:
            A :class:`~pcgs_api.schema.banknote.BanknoteImagesResponse` instance.
        """
        data = await self._get(
            "/banknotedetail/GetBanknoteImagesByCertNo",
            {"certNo": cert_no},
        )
        return BanknoteImagesResponse(**data)

    # ------------------------------------------------------------------
    # Order endpoints
    # ------------------------------------------------------------------

    async def get_orders_by_submission_no_async(
        self,
        submission_no: str,
    ) -> OrdersResponse:
        """Fetch order details for a PCGS submission number.

        Note:
            Only returns orders associated with the account that owns the
            API key.

        Args:
            submission_no: The submission identifier (e.g. ``"1234567"``).

        Returns:
            An :class:`~pcgs_api.schema.order.OrdersResponse` instance.
        """
        data = await self._get(
            "/orderdetail/GetOrdersBySubmissionNo",
            {"submissionNo": submission_no},
        )
        return OrdersResponse(**data)

    async def get_orders_by_date_range_async(
        self,
        start_date: str,
        end_date: str,
        page_no: int = 1,
        page_size: int = 10,
    ) -> OrdersResponse:
        """Fetch orders received within a date range.

        Note:
            Only returns orders associated with the account that owns the
            API key.

        Args:
            start_date: Start of date range — ``mm-dd-yyyy`` format.
            end_date: End of date range — ``mm-dd-yyyy`` format.
            page_no: 1-based page number for pagination (default ``1``).
            page_size: Number of records per page (default ``10``).

        Returns:
            An :class:`~pcgs_api.schema.order.OrdersResponse` instance.
        """
        data = await self._get(
            "/orderdetail/GetOrdersByDateRange",
            {
                "startDate": start_date,
                "endDate": end_date,
                "pageNo": page_no,
                "pageSize": page_size,
            },
        )
        return OrdersResponse(**data)
