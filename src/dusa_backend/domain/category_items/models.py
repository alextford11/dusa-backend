import uuid

from pydantic import BaseModel

from src.dusa_backend.domain.categories.models import Category
from src.dusa_backend.domain.records.models import Record


class CategoryItem(BaseModel):
    name: str
    category_id: uuid.UUID
    category: Category
    records: list[Record]
