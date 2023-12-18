from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PostRecordPayload(BaseModel):
    category_item_id: UUID
    value: Decimal
