import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.models import Record
from src.dusa_backend.domain.records.repository import RecordRepository
from src.dusa_backend.infrastructure.database.repository import get_object_or_404
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import RecordTable, CategoryItemTable
from src.dusa_backend.infrastructure.schemas.common import MessageResponse
from src.dusa_backend.infrastructure.schemas.records import PostRecordPayload, GetRecordListResponse, RecordListItem

router = APIRouter(prefix="/record", tags=["Record"])
logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_record(payload: PostRecordPayload, db_session: Session = Depends(get_db)) -> MessageResponse:
    category_item = get_object_or_404(db_session=db_session, model=CategoryItemTable, id=payload.category_item_id)
    RecordRepository(db_session).create(RecordTable(category_item=category_item, value=payload.value))
    return MessageResponse(message="Record created")


@router.get("/")
def get_records(db_session: Session = Depends(get_db)) -> GetRecordListResponse:
    records = RecordRepository(db_session).order_by(RecordTable.created.desc())[:10]
    return GetRecordListResponse(
        records=[
            RecordListItem(
                **{
                    "id": record.id,
                    "value": record.value,
                    "created": record.created,
                    "category_item_name": record.category_item.name,
                    "category_name": record.category_item.category.name,
                }
            )
            for record in records
        ]
    )
