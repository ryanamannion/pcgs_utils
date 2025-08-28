from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel
from pcgs_api.schema.image import CoinFactsImage
from pcgs_api.schema.auction import Auction


class CoinFacts(CustomBaseModel):
    pcgs_no: str = Field(alias="PCGSNo")
    cert_no: str
    name: str
    year: int
    denomination: str
    mintage: str
    mint_mark: str
    mint_location: str
    metal_content: str
    diameter: float
    edge: str
    weight: float
    country: str
    grade: str
    designation: str
    price_guide_value: float
    population: int
    pop_higher: int
    coin_facts_link: str
    designer: str
    images: list[CoinFactsImage]
    coin_facts_notes: str
    major_variety: str
    minor_variety: str
    die_variety: str
    auction_list: list[Auction]
    series_name: str
    category: str
    has_true_view_image: bool
    image_ready: bool
    is_nfc_secure: bool = Field(alias="IsNFCSecure")
    is_valid_request: bool
    server_message: str
