from enum import StrEnum

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.schemas.stats import StatsListResponse, StatsCategoryResponse
from src.dusa_backend.infrastructure.schemas.utils import TimeRangeEnum

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_stats(
    time_range: TimeRangeEnum = TimeRangeEnum.all_time, nsfw: bool = False, db_session: Session = Depends(get_db)
) -> StatsListResponse:
    if time_range == TimeRangeEnum.today:
        categories = CategoryRepository(db_session).get_todays_stats(nsfw=nsfw)
    elif time_range == TimeRangeEnum.yesterday:
        categories = CategoryRepository(db_session).get_yesterdays_stats(nsfw=nsfw)
    else:
        categories = CategoryRepository(db_session).get_all_time_stats(nsfw=nsfw)
    return StatsListResponse(stats=categories)
