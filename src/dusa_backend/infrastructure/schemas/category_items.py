from uuid import UUID

from pydantic import BaseModel


class BaseCategoryItemPayload(BaseModel):
    name: str


class CreateCategoryItemPayload(BaseCategoryItemPayload):
    category_id: UUID


class UpdateCategoryItemPayload(BaseCategoryItemPayload):
    pass
