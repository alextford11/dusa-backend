from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.repository import get_object_or_404
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import CategoryTable
from src.dusa_backend.infrastructure.schemas.categories import PostCategoryPayload, GetCategoriesResponse
from src.dusa_backend.infrastructure.schemas.common import MessageResponse

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("")
def get_categories(db_session: Session = Depends(get_db)) -> GetCategoriesResponse:
    categories = CategoryRepository(db_session).all()
    return GetCategoriesResponse(categories=categories)  # type: ignore


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: PostCategoryPayload, db_session: Session = Depends(get_db)) -> MessageResponse:
    category_repo = CategoryRepository(db_session)
    if category_repo.exists(name=payload.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category_repo.create(CategoryTable(**payload.model_dump()))
    return MessageResponse(message="Category created")


@router.post("/{category_id}")
def update_category(
    payload: PostCategoryPayload, category_id: UUID, db_session: Session = Depends(get_db)
) -> MessageResponse:
    category = get_object_or_404(db_session, CategoryTable, id=str(category_id))
    for field, value in payload.model_dump().items():
        setattr(category, field, value)

    CategoryRepository(db_session).update(category)
    return MessageResponse(message="Category updated")


@router.delete("/{category_id}")
def delete_category(category_id: UUID, db_session: Session = Depends(get_db)) -> MessageResponse:
    category = get_object_or_404(db_session, CategoryTable, id=str(category_id))
    CategoryRepository(db_session).delete(id=category.id)
    return MessageResponse(message="Category deleted")
