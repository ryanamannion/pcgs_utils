from typing import Annotated

from pydantic import Field

from pcgs_api.schema.shared import CustomBaseModel


class Image(CustomBaseModel):
    label: str
    thumbnail_url: str
    popup_url: str
    width: int = Annotated[int, Field(strict=True, ge=0)]
    height: int = Annotated[int, Field(strict=True, ge=0)]
    image_description: str = ""
