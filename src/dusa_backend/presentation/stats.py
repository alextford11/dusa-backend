from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.infrastructure.database.session import get_db
from src.dusa_backend.infrastructure.responses.stats import StatsListResponse

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", status_code=status.HTTP_200_OK, response_model=StatsListResponse)
async def get_stats(db_session: Session = Depends(get_db)):
    categories = CategoryRepository(db_session).all()
    return {"stats": categories}
