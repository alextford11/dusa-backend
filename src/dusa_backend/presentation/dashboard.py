from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.schemas.dashboards import DashboardStatsResponse, DashboardCategoryStats
from src.dusa_backend.infrastructure.schemas.stats import StatsCategoryResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_dashboard_stats(nsfw: bool = False, db_session: Session = Depends(get_db)) -> DashboardStatsResponse:
    category_repo = CategoryRepository(db_session)
    todays_categories = category_repo.get_todays_stats(nsfw=nsfw)
    yesterdays_categories = category_repo.get_yesterdays_stats(nsfw=nsfw)
    all_time_categories = category_repo.get_all_time_stats(nsfw=nsfw)
    return DashboardStatsResponse(
        stats=DashboardCategoryStats(
            today=[StatsCategoryResponse(**category.__dict__) for category in todays_categories][:3],
            yesterday=[StatsCategoryResponse(**category.__dict__) for category in yesterdays_categories][:3],
            all_time=[StatsCategoryResponse(**category.__dict__) for category in all_time_categories][:3],
        )
    )
