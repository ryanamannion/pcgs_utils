from typing import Annotated

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class Image(CustomBaseModel):
    """An image record with thumbnail and popup URLs, used in banknote responses."""

    label: str
    """Human-readable label for the image (e.g. ``"Obverse"``, ``"Reverse"``)."""

    thumbnail_url: str
    """URL of the small thumbnail image."""

    popup_url: str
    """URL of the larger popup/lightbox image."""

    width: int = Annotated[int, Field(strict=True, ge=0)]
    """Image width in pixels."""

    height: int = Annotated[int, Field(strict=True, ge=0)]
    """Image height in pixels."""

    image_description: str = ""
    """Optional descriptive caption for the image."""


class ImageSummary(CustomBaseModel):
    """A minimal image record returned by image-specific endpoints."""

    url: str
    """Direct URL to the image file."""

    resolution: str
    """Resolution descriptor (e.g. ``"thumbnail"``, ``"full"``, ``"popup"``)."""

    description: str
    """Human-readable label for the image (e.g. ``"Obverse"``, ``"TrueView"``)."""


class CoinFactsImage(CustomBaseModel):
    """Thumbnail and full-size image URLs embedded in a CoinFacts record."""

    thumbnail: str
    """URL of the thumbnail-sized image."""

    fullsize: str
    """URL of the full-resolution image."""
