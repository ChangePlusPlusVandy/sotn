from pydantic import BaseModel

from app.models.location import Region


class LocationOptions(BaseModel):
    """Choices for the intake form's location dropdowns."""

    regions: list[Region]
    counties: list[str]
