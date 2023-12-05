from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import LocationTable


class LocationRepository(BaseRepository):
    schema_class = LocationTable
