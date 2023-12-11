from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import CategoryTable


class CategoryRepository(BaseRepository):
    model = CategoryTable
