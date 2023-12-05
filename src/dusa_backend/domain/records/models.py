import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from src.dusa_backend.domain.category_items.models import CategoryItem


class Record(BaseModel):
    created: datetime
    value: Decimal
    nsfw: bool
    category_item_id: uuid.UUID
    category_item: CategoryItem
