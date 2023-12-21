from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.dusa_backend.domain.models import Location


class PostLocationPayload(BaseModel):
    latitude: Decimal
    longitude: Decimal


class ListLocationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locations: list[Location]
