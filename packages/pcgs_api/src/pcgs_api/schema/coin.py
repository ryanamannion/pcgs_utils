from typing import Optional

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class CoinFactsImage(CustomBaseModel):
    thumbnail: Optional[str] = None
    fullsize: Optional[str] = None


class AuctionItem(CustomBaseModel):
    service: Optional[str] = None
    date: Optional[str] = None
    auctioneer: Optional[str] = None
    lot_no: Optional[int] = None
    lot_num_v2: Optional[str] = None
    sale_name: Optional[str] = None
    cert_no: Optional[str] = None
    price: Optional[float] = None
    is_cac: Optional[bool] = Field(None, alias="IsCAC")
    auction_lot_url: Optional[str] = None


class CoinFacts(CustomBaseModel):
    """Coin data returned by GetCoinFactsByCertNo, GetCoinFactsByGrade,
    and GetCoinFactsByBarcode. Field availability varies by endpoint."""

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    cert_no: Optional[str] = None
    name: Optional[str] = None
    year: Optional[int] = None
    denomination: Optional[str] = None
    mintage: Optional[str] = None
    mint_mark: Optional[str] = None
    mint_location: Optional[str] = None
    metal_content: Optional[str] = None
    diameter: Optional[float] = None
    edge: Optional[str] = None
    weight: Optional[float] = None
    country: Optional[str] = None
    grade: Optional[str] = None
    designation: Optional[str] = None
    price_guide_value: Optional[float] = None
    population: Optional[int] = None
    pop_higher: Optional[int] = None
    coin_facts_link: Optional[str] = None
    designer: Optional[str] = None
    images: Optional[list[CoinFactsImage]] = None
    coin_facts_notes: Optional[str] = None
    major_variety: Optional[str] = None
    minor_variety: Optional[str] = None
    die_variety: Optional[str] = None
    auction_list: Optional[list[AuctionItem]] = None
    series_name: Optional[str] = None
    category: Optional[str] = None
    # Present on GetCoinFactsByCertNo and GetCoinFactsByBarcode
    has_true_view_image: Optional[bool] = None
    has_obverse_image: Optional[bool] = None
    has_reverse_image: Optional[bool] = None
    image_ready: Optional[bool] = None
    is_nfc_secure: Optional[bool] = Field(None, alias="IsNFCSecure")
    is_valid_request: bool
    server_message: str


class AuctionResponse(CustomBaseModel):
    """Response from GetAPRByCertNo. Includes cert-specific fields."""

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    cert_no: Optional[str] = None
    name: Optional[str] = None
    grade: Optional[str] = None
    year: Optional[str] = None
    denomination: Optional[str] = None
    auctions: Optional[list[AuctionItem]] = None
    is_valid_request: bool
    server_message: Optional[str] = None


class AuctionListResponse(CustomBaseModel):
    """Response from GetAPRByGrade and GetAPRByBarcode."""

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    name: Optional[str] = None
    year: Optional[str] = None
    denomination: Optional[str] = None
    auctions: Optional[list[AuctionItem]] = None
    is_valid_request: bool
    server_message: Optional[str] = None


class ImageDetail(CustomBaseModel):
    """A single image entry returned by GetImagesByCertNo."""

    url: Optional[str] = None
    resolution: Optional[str] = None
    description: Optional[str] = None


class CoinImagesResponse(CustomBaseModel):
    """Response from GetImagesByCertNo."""

    cert_no: Optional[str] = None
    images: Optional[list[ImageDetail]] = None
    has_obverse_image: bool = False
    has_reverse_image: bool = False
    has_true_view_image: bool = False
    image_ready: bool = False
    is_valid_request: bool
    server_message: str
