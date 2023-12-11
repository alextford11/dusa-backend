from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created: datetime
    value: Decimal
    nsfw: bool


class CategoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    records: list[Record]


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    category_items: list[CategoryItem]


class Location(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created: datetime
    longitude: Decimal
    latitude: Decimal
