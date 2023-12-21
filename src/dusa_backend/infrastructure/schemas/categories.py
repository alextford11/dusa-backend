from pydantic import BaseModel, ConfigDict

from src.dusa_backend.domain.models import Category


class PostCategoryPayload(BaseModel):
    name: str
    nsfw: bool


class GetCategoriesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    categories: list[Category]
