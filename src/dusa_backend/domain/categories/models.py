from pydantic import BaseModel

from src.dusa_backend.domain.category_items.models import CategoryItem


class Category(BaseModel):
    name: str
    category_items: list[CategoryItem]
