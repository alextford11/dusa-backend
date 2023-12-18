from pydantic import BaseModel, ConfigDict


class StatsCategoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    records_value_sum: int


class StatsCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    category_items: list[StatsCategoryItemResponse]


class StatsListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stats: list[StatsCategoryResponse]


class DashboardCategoryStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    today: list[StatsCategoryResponse]
    yesterday: list[StatsCategoryResponse]
    all_time: list[StatsCategoryResponse]


class DashboardStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stats: DashboardCategoryStats
