from datetime import datetime, timedelta

from sqlalchemy.orm import contains_eager, Query

from src.dusa_backend.infrastructure.database.repository import BaseRepository
from src.dusa_backend.infrastructure.database.tables import CategoryTable, CategoryItemTable, RecordTable


from sqlalchemy.orm import aliased

filtered_records_alias = aliased(RecordTable)


class CategoryRepository(BaseRepository):
    model = CategoryTable

    def _query_categories(self, start_of_day: datetime | None, end_of_day: datetime | None, nsfw: bool) -> Query:
        query = self.db_session.query(self.model).join(CategoryItemTable).join(filtered_records_alias)
        if not nsfw:
            # exclude categories that have nsfw equal to true when nsfw passed is false
            query = query.filter(~self.model.nsfw.is_(True))

        if start_of_day and end_of_day:
            query = query.filter(filtered_records_alias.created.between(start_of_day, end_of_day))

        query = query.options(
            contains_eager(self.model.category_items, CategoryItemTable.records, alias=filtered_records_alias)
        )
        return query

    def get_todays_stats(self, nsfw: bool = False) -> Query:
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0)
        end_of_day = now.replace(hour=23, minute=59, second=59)
        return self._query_categories(start_of_day=start_of_day, end_of_day=end_of_day, nsfw=nsfw)

    def get_yesterdays_stats(self, nsfw: bool = False) -> Query:
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_of_day = yesterday.replace(hour=0, minute=0, second=0)
        end_of_day = yesterday.replace(hour=23, minute=59, second=59)
        return self._query_categories(start_of_day=start_of_day, end_of_day=end_of_day, nsfw=nsfw)

    def get_all_time_stats(self, nsfw: bool = False) -> Query:
        return self._query_categories(start_of_day=None, end_of_day=None, nsfw=nsfw)
