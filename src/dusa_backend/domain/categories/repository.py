from datetime import datetime, timedelta

from sqlalchemy.orm import contains_eager

from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import CategoryTable, CategoryItemTable, RecordTable


from sqlalchemy.orm import aliased


class CategoryRepository(BaseRepository):
    model = CategoryTable

    def _query_categories_between_datetimes(self, start_of_day, end_of_day):
        filtered_records_alias = aliased(RecordTable)
        return (
            self.db_session.query(CategoryTable)
            .join(CategoryItemTable)
            .join(filtered_records_alias)
            .filter(filtered_records_alias.created.between(start_of_day, end_of_day))
            .options(
                contains_eager(CategoryTable.category_items, CategoryItemTable.records, alias=filtered_records_alias)
            )
        )

    def get_todays_stats(self):
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0)
        end_of_day = now.replace(hour=23, minute=59, second=59)
        return self._query_categories_between_datetimes(start_of_day, end_of_day)

    def get_yesterdays_stats(self):
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_of_day = yesterday.replace(hour=0, minute=0, second=0)
        end_of_day = yesterday.replace(hour=23, minute=59, second=59)
        return self._query_categories_between_datetimes(start_of_day, end_of_day)
