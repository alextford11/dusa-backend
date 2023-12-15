from enum import StrEnum

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.responses.stats import StatsListResponse

router = APIRouter(prefix="/stats", tags=["Stats"])


class TimeRangeEnum(StrEnum):
    today = "today"
    yesterday = "yesterday"
    all_time = "all_time"


@router.get("", status_code=status.HTTP_200_OK)
async def get_stats(
    time_range: TimeRangeEnum = TimeRangeEnum.all_time, db_session: Session = Depends(get_db)
) -> StatsListResponse:
    if time_range == TimeRangeEnum.today:
        categories = CategoryRepository(db_session).get_todays_stats()
    elif time_range == TimeRangeEnum.yesterday:
        categories = CategoryRepository(db_session).get_yesterdays_stats()
    else:
        categories = CategoryRepository(db_session).all()
    return StatsListResponse(stats=categories)
