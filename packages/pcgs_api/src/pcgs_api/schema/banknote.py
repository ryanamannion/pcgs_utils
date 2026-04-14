from typing import Annotated, Optional

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel
from pcgs_api.schema.image import Image, ImageSummary


class Banknote(CustomBaseModel):
    """Details for a single PMG/PCGS-certified banknote."""

    pcgs_no: str = Field(alias="PCGSNo")
    """PCGS specification number identifying the banknote type."""

    cert_no: str
    """Certificate number printed on the PMG/PCGS holder."""

    year: str
    """Year of issue or date range (e.g. ``"1934"``, ``"1934A"``)."""

    denomination: str
    """Face value denomination (e.g. ``"$100"``, ``"1 Pound"``)."""

    region: str
    """Issuing region or country (e.g. ``"United States of America"``)."""

    grade: str
    """Full grade string (e.g. ``"Choice Uncirculated 64"``)."""

    details: str
    """Details qualifier, if any (e.g. ``"Restoration"``, ``"Stains"``)."""

    population: Annotated[int, Field(strict=True, ge=0)]
    """Number of examples graded at this grade level (population report)."""

    pop_higher: Annotated[int, Field(strict=True, ge=0)]
    """Number of examples graded *above* this grade level."""

    serial_no: str
    """Serial number printed on the banknote."""

    height: str
    """Note height in millimetres."""

    width: str
    """Note width in millimetres."""

    images: list[Image]
    """Thumbnail and popup image URLs for the obverse and reverse."""

    catalog_no_1: str
    """Primary catalogue reference number (e.g. Friedberg number for US notes)."""

    catalog_no_2: str
    """Secondary catalogue reference number."""

    catalog_1_long_desc: str
    """Full name / long description of the primary catalogue."""

    catalog_2_long_desc: str
    """Full name / long description of the secondary catalogue."""

    catalog_1_short_desc: str
    """Abbreviated label for the primary catalogue."""

    catalog_2_short_desc: str
    """Abbreviated label for the secondary catalogue."""

    signers: str
    """Names of the signatories printed on the note (Treasurer and Secretary)."""

    qualifiers: str
    """Any additional qualifiers applied to the grade."""

    plate_no: str
    """Plate or check letter/number identifying the printing plate."""

    value_view_link: str
    """URL to the PCGS ValueView page for this banknote type."""

    has_obverse_image: bool
    """``True`` if an obverse image is available."""

    has_reverse_image: bool
    """``True`` if a reverse image is available."""

    image_ready: bool
    """``True`` if images have been processed and are ready to display."""


class BanknoteResponse(CustomBaseModel):
    """Response from ``GetBanknoteByCertNo``.

    Wraps a single :class:`Banknote` record identified by its certificate
    number.
    """

    banknote: Optional[Banknote] = None
    """The matched banknote record, or ``None`` if not found."""

    is_valid_request: bool
    """``True`` when the API call succeeded and the certificate was found."""

    server_message: str
    """Human-readable status or error message from the API server."""


class BanknotesResponse(CustomBaseModel):
    """Response from ``GetBanknoteByGrade``.

    Returns all certified banknotes matching a given specification number and
    grade.
    """

    banknotes: Optional[list[Banknote]] = None
    """List of matching banknote records."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: str
    """Human-readable status or error message from the API server."""


class BanknoteImagesResponse(CustomBaseModel):
    """Response from ``GetBanknoteImagesByCertNo``.

    Contains all available images for a certified banknote along with
    availability flags.
    """

    cert_no: str
    """Certificate number that was queried."""

    images: list[ImageSummary]
    """All image records available for this banknote."""

    has_obverse_image: bool
    """``True`` if an obverse image is available."""

    has_reverse_image: bool
    """``True`` if a reverse image is available."""

    has_true_view_image: bool
    """``True`` if a high-resolution TrueView image is available."""

    image_ready: bool
    """``True`` if images have been processed and are ready to display."""

    is_valid_request: bool
    """``True`` when the API call succeeded."""

    server_message: str
    """Human-readable status or error message from the API server."""
