from pydantic import BaseModel, ConfigDict

from src.dusa_backend.infrastructure.schemas.stats import StatsCategoryResponse


class DashboardCategoryStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    today: list[StatsCategoryResponse]
    yesterday: list[StatsCategoryResponse]
    all_time: list[StatsCategoryResponse]


class DashboardStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stats: DashboardCategoryStats
