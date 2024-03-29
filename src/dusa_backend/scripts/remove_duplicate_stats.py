from dusa_backend.domain.categories.repository import CategoryRepository
from dusa_backend.domain.records.repository import RecordRepository
from dusa_backend.infrastructure.database.session import SessionLocal
from dusa_backend.infrastructure.database.tables import RecordTable


def remove_duplicate_health_stats():
    with SessionLocal() as db_session:
        record_repo = RecordRepository(db_session)
        category_repo = CategoryRepository(db_session)

        health_category = category_repo.get(name="Health")
        for category_item in health_category.category_items:
            records = (
                db_session.query(RecordTable)
                .join(RecordTable.category_item)
                .filter(RecordTable.category_item_id == category_item.id)
                .order_by(RecordTable.value.desc())
            )
            dates_found = set()
            delete_count = 0
            for record in records:
                if record.created.date() in dates_found:
                    delete_count += record_repo.delete(id=record.id)
                else:
                    dates_found.add(record.created.date())
            print(f"Deleted {delete_count} records for {category_item.name} category item")
