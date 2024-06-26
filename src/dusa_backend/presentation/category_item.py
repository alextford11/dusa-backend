from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.infrastructure.database.repository import get_object_or_404
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import CategoryItemTable
from src.dusa_backend.infrastructure.schemas.category_items import CreateCategoryItemPayload, UpdateCategoryItemPayload
from src.dusa_backend.infrastructure.schemas.common import MessageResponse

router = APIRouter(prefix="/category_item", tags=["Category Item"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category_item(payload: CreateCategoryItemPayload, db_session: Session = Depends(get_db)) -> MessageResponse:
    category_item_repo = CategoryItemRepository(db_session)
    if category_item_repo.exists(**payload.model_dump()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Item already exists")
    category_item_repo.create(CategoryItemTable(**payload.model_dump()))
    return MessageResponse(message="Category Item created")


@router.post("/{category_item_id}")
def update_category(
    payload: UpdateCategoryItemPayload, category_item_id: UUID, db_session: Session = Depends(get_db)
) -> MessageResponse:
    category_item = get_object_or_404(db_session, CategoryItemTable, id=str(category_item_id))
    for field, value in payload.model_dump().items():
        setattr(category_item, field, value)

    CategoryItemRepository(db_session).update(category_item)
    return MessageResponse(message="Category Item updated")


@router.delete("/{category_item_id}")
def delete_category_item(category_item_id: UUID, db_session: Session = Depends(get_db)) -> MessageResponse:
    category_item = get_object_or_404(db_session, CategoryItemTable, id=str(category_item_id))
    CategoryItemRepository(db_session).delete(id=category_item.id)
    return MessageResponse(message="Category Item deleted")
