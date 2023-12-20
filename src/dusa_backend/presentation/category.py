from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.repository import get_object_or_404
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import CategoryTable
from src.dusa_backend.infrastructure.schemas.categories import PostCategoryPayload

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(payload: PostCategoryPayload, db_session: Session = Depends(get_db)) -> dict:
    category_repo = CategoryRepository(db_session)
    if category_repo.exists(name=payload.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category_repo.create(CategoryTable(**payload.model_dump()))
    return {"message": "Category created"}


@router.delete("/{category_id}")
def delete_category(category_id: UUID, db_session: Session = Depends(get_db)):
    category = get_object_or_404(db_session, CategoryTable, id=str(category_id))
    CategoryRepository(db_session).delete(id=category.id)
    return {"message": "Category deleted"}
