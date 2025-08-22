from typing import Annotated, Optional

from pydantic import Field, conint

from pcgs_api.schema.shared import CustomBaseModel
from pcgs_api.schema.image import Image, ImageSummary


class Banknote(CustomBaseModel):
    pcgs_no: str = Field(alias="PCGSNo")
    cert_no: str
    year: str
    denomination: str
    region: str
    grade: str
    details: str
    population: Annotated[int, Field(strict=True, ge=0)]
    pop_higher: Annotated[int, Field(strict=True, ge=0)]
    serial_no: str
    height: str
    width: str
    images: list[Image]
    catalog_no_1: str
    catalog_no_2: str
    catalog_1_long_desc: str
    catalog_2_long_desc: str
    catalog_1_short_desc: str
    catalog_2_short_desc: str
    signers: str
    qualifiers: str
    plate_no: str
    value_view_link: str
    has_obverse_image: bool
    has_reverse_image: bool
    image_ready: bool


class BanknoteResponse(CustomBaseModel):
    banknote: Optional[Banknote] = None
    is_valid_request: bool
    server_message: str


class BanknotesResponse(CustomBaseModel):
    banknotes: Optional[list[Banknote]] = None
    is_valid_request: bool
    server_message: str


class BanknoteImagesResponse(CustomBaseModel):
    cert_no: str
    images: list[ImageSummary]
    has_obverse_image: bool
    has_reverse_image: bool
    has_true_view_image: bool
    image_ready: bool
    is_valid_request: bool
    server_message: str
