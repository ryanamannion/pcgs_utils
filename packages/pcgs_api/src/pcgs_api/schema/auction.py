from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class Auction(CustomBaseModel):
    service: str
    date: str
    auctioneer: str
    lot_no: int
    lot_num_v2: str
    sale_name: str
    cert_no: str
    price: float
    is_cac: bool = Field(alias="IsCAC")
    auction_lot_url: str


class AuctionPricesRealized(CustomBaseModel):
    pcgs_no: str = Field(alias="PCGSNo")
    cert_no: str
    name: str
    grade: str
    year: int
    denomination: str
    auctions: list[Auction]
    is_valid_request: bool
    server_message: str