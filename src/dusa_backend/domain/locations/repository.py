from datetime import datetime, timedelta

from sqlalchemy.orm import Query

from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import LocationTable


class LocationRepository(BaseRepository):
    model = LocationTable

    def _locations_query(self, start_of_day: datetime, end_of_day: datetime) -> Query:
        return self.filter(self.model.created.between(start_of_day, end_of_day)).order_by(LocationTable.created.asc())

    def get_todays_locations(self):
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0)
        end_of_day = now.replace(hour=23, minute=59, second=59)
        return self._locations_query(start_of_day=start_of_day, end_of_day=end_of_day)

    def get_yesterdays_locations(self):
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_of_day = yesterday.replace(hour=0, minute=0, second=0)
        end_of_day = yesterday.replace(hour=23, minute=59, second=59)
        return self._locations_query(start_of_day=start_of_day, end_of_day=end_of_day)

    def get_all_locations(self):
        return self.order_by(LocationTable.created.asc())
