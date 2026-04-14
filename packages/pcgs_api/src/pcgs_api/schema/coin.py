from typing import Optional

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class CoinFactsImage(CustomBaseModel):
    """Obverse/reverse image URLs for a coin in a :class:`CoinFacts` response."""

    thumbnail: Optional[str] = None
    """URL of the thumbnail-sized image."""

    fullsize: Optional[str] = None
    """URL of the full-resolution image."""


class AuctionItem(CustomBaseModel):
    """A single auction price realized record."""

    service: Optional[str] = None
    """Grading service that certified the coin (e.g. ``"PCGS"``)."""

    date: Optional[str] = None
    """Date the auction lot was sold (``mm/dd/yyyy``)."""

    auctioneer: Optional[str] = None
    """Name of the auction house (e.g. ``"Heritage Auctions"``)."""

    lot_no: Optional[int] = None
    """Numeric lot number within the sale."""

    lot_num_v2: Optional[str] = None
    """Alphanumeric lot identifier used by some auction houses."""

    sale_name: Optional[str] = None
    """Name or identifier of the auction sale event."""

    cert_no: Optional[str] = None
    """Certificate number of the coin that sold."""

    price: Optional[float] = None
    """Hammer price in USD (before buyer's premium unless noted)."""

    is_cac: Optional[bool] = Field(None, alias="IsCAC")
    """``True`` if the coin carried a CAC (Certified Acceptance Corporation) sticker."""

    auction_lot_url: Optional[str] = None
    """Direct URL to the auction lot page."""


class CoinFacts(CustomBaseModel):
    """Coin data returned by ``GetCoinFactsByCertNo``, ``GetCoinFactsByGrade``,
    and ``GetCoinFactsByBarcode``.

    Not every field is populated by every endpoint.  Fields related to images
    and auction history are only present when ``retrieve_all_data=True`` is
    passed to ``GetCoinFactsByCertNo``.
    """

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    """PCGS specification (catalogue) number identifying the coin type."""

    cert_no: Optional[str] = None
    """Certificate number printed on the PCGS holder (7–8 digits)."""

    name: Optional[str] = None
    """Full descriptive name of the coin (e.g. ``"1921 $1 Morgan Dollar MS65"``)."""

    year: Optional[int] = None
    """Year of issue."""

    denomination: Optional[str] = None
    """Face value denomination (e.g. ``"$1"``, ``"25C"``)."""

    mintage: Optional[str] = None
    """Total number of coins struck for this date/mint combination."""

    mint_mark: Optional[str] = None
    """Mint mark letter, if any (e.g. ``"S"``, ``"D"``)."""

    mint_location: Optional[str] = None
    """Full name of the mint facility (e.g. ``"San Francisco"``)."""

    metal_content: Optional[str] = None
    """Alloy composition (e.g. ``"90% Silver, 10% Copper"``)."""

    diameter: Optional[float] = None
    """Coin diameter in millimetres."""

    edge: Optional[str] = None
    """Edge description (e.g. ``"Reeded"``, ``"Plain"``)."""

    weight: Optional[float] = None
    """Coin weight in grams."""

    country: Optional[str] = None
    """Country of issue."""

    grade: Optional[str] = None
    """Full PCGS grade string (e.g. ``"MS65"``, ``"PR69DCAM"``)."""

    designation: Optional[str] = None
    """Special designation, if any (e.g. ``"CAMEO"``, ``"DMPL"``)."""

    price_guide_value: Optional[float] = None
    """Current PCGS Price Guide value in USD for this grade."""

    population: Optional[int] = None
    """Number of examples graded at this grade level (population report)."""

    pop_higher: Optional[int] = None
    """Number of examples graded *above* this grade level."""

    coin_facts_link: Optional[str] = None
    """URL to the CoinFacts detail page for this specification."""

    designer: Optional[str] = None
    """Name of the coin's designer/engraver."""

    images: Optional[list[CoinFactsImage]] = None
    """Obverse and reverse image URLs. Populated when ``retrieve_all_data=True``."""

    coin_facts_notes: Optional[str] = None
    """Editorial notes from the CoinFacts database."""

    major_variety: Optional[str] = None
    """Major die variety designation (e.g. ``"8 Tail Feathers"``)."""

    minor_variety: Optional[str] = None
    """Minor die variety designation."""

    die_variety: Optional[str] = None
    """Specific die variety (e.g. VAM number for Morgan dollars)."""

    auction_list: Optional[list[AuctionItem]] = None
    """Historical auction prices realized. Populated when ``retrieve_all_data=True``."""

    series_name: Optional[str] = None
    """Name of the coin series (e.g. ``"Morgan Dollar"``)."""

    category: Optional[str] = None
    """Broad category (e.g. ``"Dollars"``)."""

    has_true_view_image: Optional[bool] = None
    """``True`` if a PCGS TrueView® high-resolution image exists."""

    has_obverse_image: Optional[bool] = None
    """``True`` if an obverse image is available."""

    has_reverse_image: Optional[bool] = None
    """``True`` if a reverse image is available."""

    image_ready: Optional[bool] = None
    """``True`` if images have been processed and are ready to display."""

    is_nfc_secure: Optional[bool] = Field(None, alias="IsNFCSecure")
    """``True`` if the holder contains an NFC security chip."""

    is_valid_request: bool
    """``True`` when the API call succeeded and the coin was found."""

    server_message: str
    """Human-readable status or error message from the API server."""


class AuctionResponse(CustomBaseModel):
    """Response from ``GetAPRByCertNo``.

    Returns auction prices realized for a specific certified coin identified
    by its certificate number.
    """

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    """PCGS specification number for the coin type."""

    cert_no: Optional[str] = None
    """Certificate number that was queried."""

    name: Optional[str] = None
    """Descriptive name of the coin."""

    grade: Optional[str] = None
    """PCGS grade string (e.g. ``"MS65"``)."""

    year: Optional[str] = None
    """Year of issue."""

    denomination: Optional[str] = None
    """Face value denomination."""

    auctions: Optional[list[AuctionItem]] = None
    """List of auction price realized records for this specific coin."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: Optional[str] = None
    """Human-readable status or error message from the API server."""


class AuctionListResponse(CustomBaseModel):
    """Response from ``GetAPRByGrade`` and ``GetAPRByBarcode``.

    Returns a list of auction prices realized across all examples of a coin
    type at a given grade, rather than a single certified coin.
    """

    pcgs_no: Optional[str] = Field(None, alias="PCGSNo")
    """PCGS specification number for the coin type."""

    name: Optional[str] = None
    """Descriptive name of the coin type."""

    year: Optional[str] = None
    """Year of issue."""

    denomination: Optional[str] = None
    """Face value denomination."""

    auctions: Optional[list[AuctionItem]] = None
    """List of auction price realized records across all matching coins."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: Optional[str] = None
    """Human-readable status or error message from the API server."""


class ImageDetail(CustomBaseModel):
    """A single image entry returned by ``GetImagesByCertNo``."""

    url: Optional[str] = None
    """Direct URL to the image file."""

    resolution: Optional[str] = None
    """Image resolution descriptor (e.g. ``"thumbnail"``, ``"full"``)."""

    description: Optional[str] = None
    """Human-readable label for the image (e.g. ``"Obverse"``, ``"TrueView"``)."""


class CoinImagesResponse(CustomBaseModel):
    """Response from ``GetImagesByCertNo``.

    Contains all available images for a certified coin along with availability
    flags for each image type.
    """

    cert_no: Optional[str] = None
    """Certificate number that was queried."""

    images: Optional[list[ImageDetail]] = None
    """All image records available for this coin."""

    has_obverse_image: bool = False
    """``True`` if an obverse image is available."""

    has_reverse_image: bool = False
    """``True`` if a reverse image is available."""

    has_true_view_image: bool = False
    """``True`` if a PCGS TrueView® high-resolution image is available."""

    image_ready: bool = False
    """``True`` if images have been processed and are ready to display."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: str
    """Human-readable status or error message from the API server."""
