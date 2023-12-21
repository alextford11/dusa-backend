from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.locations.repository import LocationRepository
from src.dusa_backend.domain.models import Location
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import LocationTable
from src.dusa_backend.infrastructure.schemas.common import MessageResponse
from src.dusa_backend.infrastructure.schemas.locations import PostLocationPayload, ListLocationsResponse
from src.dusa_backend.infrastructure.schemas.utils import TimeRangeEnum

router = APIRouter(prefix="/location", tags=["location"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_location(payload: PostLocationPayload, db_session: Session = Depends(get_db)) -> MessageResponse:
    LocationRepository(db_session).create(LocationTable(**payload.model_dump()))
    return MessageResponse(message="Location created")


@router.get("/list")
def get_locations(
    time_range: TimeRangeEnum = TimeRangeEnum.all_time, db_session: Session = Depends(get_db)
) -> ListLocationsResponse:
    location_repo = LocationRepository(db_session)
    if time_range == TimeRangeEnum.today:
        locations = location_repo.get_todays_locations()
    elif time_range == TimeRangeEnum.yesterday:
        locations = location_repo.get_yesterdays_locations()
    else:
        locations = location_repo.get_all_locations()
    return ListLocationsResponse(locations=locations)


@router.get("/recent")
def get_most_recent_location(db_session: Session = Depends(get_db)) -> Location | dict:
    return LocationRepository(db_session).order_by(LocationTable.created.desc()).limit(1).one_or_none() or {}
