from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal

__all__ = ["CustomBaseModel"]


class CustomBaseModel(BaseModel):
    """Base model with shared customizations for PCGS API"""

    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True
    )
