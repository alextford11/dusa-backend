from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import RecordTable


class RecordRepository(BaseRepository):
    model = RecordTable
