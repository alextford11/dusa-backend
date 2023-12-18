from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.responses.stats import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_dashboard_stats(db_session: Session = Depends(get_db)) -> DashboardStatsResponse:
    category_repo = CategoryRepository(db_session)
    todays_categories = category_repo.get_todays_stats()[:5]
    yesterdays_categories = category_repo.get_yesterdays_stats()[:5]
    all_time_categories = category_repo.all()[:5]
    return DashboardStatsResponse(
        stats={"today": todays_categories, "yesterday": yesterdays_categories, "all_time": all_time_categories}
    )
