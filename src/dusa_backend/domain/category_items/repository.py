
from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import CategoryItemTable


class CategoryItemRepository(BaseRepository):
    model = CategoryItemTable
