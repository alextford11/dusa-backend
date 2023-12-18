from uuid import UUID

from pydantic import BaseModel


class PostCategoryItemPayload(BaseModel):
    name: str
    category_id: UUID
