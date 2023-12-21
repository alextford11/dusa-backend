from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatsCategoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    records_value_sum: Decimal


class StatsCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category_items: list[StatsCategoryItemResponse]


class StatsListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stats: list[StatsCategoryResponse]
