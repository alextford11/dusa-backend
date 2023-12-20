from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import CategoryItemTable
from src.dusa_backend.infrastructure.schemas.category_items import PostCategoryItemPayload

router = APIRouter(prefix="/category_item", tags=["Category"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category_item(payload: PostCategoryItemPayload, db_session: Session = Depends(get_db)) -> dict:
    category_item_repo = CategoryItemRepository(db_session)
    if category_item_repo.exists(**payload.model_dump()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Item already exists")
    category_item_repo.create(CategoryItemTable(**payload.model_dump()))
    return {"message": "Category Item created"}
