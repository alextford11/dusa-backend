from pydantic import BaseModel


class PostCategoryPayload(BaseModel):
    name: str
    nsfw: bool
