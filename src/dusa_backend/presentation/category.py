from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.database.tables import CategoryTable
from src.dusa_backend.infrastructure.schemas.categories import PostCategoryPayload

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(payload: PostCategoryPayload, db_session: Session = Depends(get_db)) -> dict:
    category_repo = CategoryRepository(db_session)
    if category_repo.exists(name=payload.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category_repo.create(CategoryTable(name=payload.name))
    return {"message": "Category created"}
