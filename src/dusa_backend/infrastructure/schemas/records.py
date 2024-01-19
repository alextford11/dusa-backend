from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.dusa_backend.domain.models import Record


class PostRecordPayload(BaseModel):
    category_item_id: UUID
    value: Decimal


class RecordListItem(Record):
    category_item_name: str
    category_name: str


class GetRecordListResponse(BaseModel):
    records: list[RecordListItem]
