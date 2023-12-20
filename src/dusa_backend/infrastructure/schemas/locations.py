from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class LocationObject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latitude: Decimal
    longitude: Decimal


class PostLocationPayload(LocationObject):
    pass


class ListLocationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locations: list[LocationObject]
