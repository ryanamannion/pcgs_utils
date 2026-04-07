from typing import Optional

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class GradingOrderLine(CustomBaseModel):
    line_no: Optional[int] = None
    item_no: Optional[int] = None
    cert_no: Optional[str] = None
    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    description: Optional[str] = None
    display_grade: Optional[str] = None
    country: Optional[str] = None
    images: Optional[list[str]] = None


class OrderDetail(CustomBaseModel):
    submission_no: Optional[str] = None
    order_no: Optional[str] = None
    customer_no: Optional[str] = None
    item_count: Optional[int] = None
    service: Optional[str] = None
    order_status: Optional[str] = None
    date_received: Optional[str] = None
    date_shipped: Optional[str] = None
    courier: Optional[str] = None
    tracking_no: Optional[str] = None
    tracking_url: Optional[str] = None
    is_cancelled: Optional[bool] = None
    image_in_process: Optional[bool] = None
    image_ready: Optional[bool] = None
    grade_ready: Optional[bool] = None
    order_lines: Optional[list[GradingOrderLine]] = None


class OrdersResponse(CustomBaseModel):
    orders: Optional[list[OrderDetail]] = None
    is_valid_request: bool
    server_message: str
