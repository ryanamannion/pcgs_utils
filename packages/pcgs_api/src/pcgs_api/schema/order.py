from typing import Optional

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class GradingOrderLine(CustomBaseModel):
    """A single line item within a PCGS grading submission order."""

    line_no: Optional[int] = None
    """Sequential line number within the submission."""

    item_no: Optional[int] = None
    """Item number assigned by PCGS during processing."""

    cert_no: Optional[str] = None
    """Certificate number assigned to the graded coin, once graded."""

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    """PCGS specification number of the graded coin."""

    description: Optional[str] = None
    """Full descriptive name and grade of the coin."""

    display_grade: Optional[str] = None
    """Human-readable grade string (e.g. ``"MS65"``, ``"Genuine"``)."""

    country: Optional[str] = None
    """Country of origin for the coin."""

    images: Optional[list[str]] = None
    """URLs of available images for this line item."""


class OrderDetail(CustomBaseModel):
    """Details for a single PCGS grading submission order."""

    submission_no: Optional[str] = None
    """PCGS submission number (primary reference for a grading order)."""

    order_no: Optional[str] = None
    """Internal order number assigned by PCGS."""

    customer_no: Optional[str] = None
    """PCGS customer account number associated with this order."""

    item_count: Optional[int] = None
    """Total number of coins included in the submission."""

    service: Optional[str] = None
    """Grading service tier selected (e.g. ``"Economy"``, ``"Regular"``)."""

    order_status: Optional[str] = None
    """Current processing status (e.g. ``"Received"``, ``"Grading"``, ``"Shipped"``)."""

    date_received: Optional[str] = None
    """Date PCGS received the submission (``mm/dd/yyyy``)."""

    date_shipped: Optional[str] = None
    """Date PCGS shipped the completed order back (``mm/dd/yyyy``)."""

    courier: Optional[str] = None
    """Shipping carrier used for return delivery."""

    tracking_no: Optional[str] = None
    """Carrier tracking number for the return shipment."""

    tracking_url: Optional[str] = None
    """Direct URL to the carrier tracking page."""

    is_cancelled: Optional[bool] = None
    """``True`` if this order has been cancelled."""

    image_in_process: Optional[bool] = None
    """``True`` if coin imaging is currently in progress."""

    image_ready: Optional[bool] = None
    """``True`` if coin images have been processed and are available."""

    grade_ready: Optional[bool] = None
    """``True`` if grading is complete and grades are available."""

    order_lines: Optional[list[GradingOrderLine]] = None
    """Individual line items (coins) within this submission."""


class OrdersResponse(CustomBaseModel):
    """Response from ``GetOrdersBySubmissionNo`` and ``GetOrdersByDateRange``.

    Contains one or more :class:`OrderDetail` records matching the query.
    Only orders belonging to the authenticated account are returned.
    """

    orders: Optional[list[OrderDetail]] = None
    """List of matching grading submission orders."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: str
    """Human-readable status or error message from the API server."""
