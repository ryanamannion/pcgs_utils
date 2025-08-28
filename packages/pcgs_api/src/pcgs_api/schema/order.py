from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class OrderLine(CustomBaseModel):
    line_no: int
    item_no: int
    cert_no: str
    pcgs_no: str = Field(alias="PCGSNo")
    description: str
    display_grade: str
    country: str
    images: list[str]

class Order(CustomBaseModel):
    submission_no: str
    order_no: str
    customer_no: str
    item_count: int
    order_status: str
    date_received: str  # TODO: parse as datetime?
    date_shipped: str
    courier: str
    tracking_no: str
    tracking_url: str
    is_cancelled: bool
    image_in_process: bool
    image_ready: bool
    grade_ready: bool
    order_lines: list[OrderLine]


class OrdersResponse(CustomBaseModel):
    orders: list[Order]
    is_valid_request: bool
    server_message: str


