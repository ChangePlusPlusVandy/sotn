from fastapi import APIRouter

from app.models.location import TN_COUNTIES, Region
from app.schemas.location import LocationOptions

# Public router: no authentication required
router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=LocationOptions)
def get_locations():
    """Regions and counties, so the intake form doesn't keep its own copy."""
    return LocationOptions(regions=list(Region), counties=list(TN_COUNTIES))
