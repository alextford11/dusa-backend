from dusa_backend.domain.category_items.repository import CategoryItemRepository
from dusa_backend.domain.records.repository import RecordRepository
from dusa_backend.infrastructure.database.session import SessionLocal
from dusa_backend.infrastructure.database.tables import RecordTable


ATM_RECORD_IDS = [
    "b1444629-e086-40cf-a012-c97760a4f932",
    "74c49e90-b688-42ee-8c99-8b5fed101ccb",
    "b00e04b6-45ee-43bd-8db0-4b1fb40b4ea7",
]


def atm_records_fix():
    with SessionLocal() as db_session:
        record_repo = RecordRepository(db_session)
        category_item_repo = CategoryItemRepository(db_session)

        atm_category_item = category_item_repo.get(name="ATM")
        records = db_session.query(RecordTable).filter(RecordTable.id.in_(ATM_RECORD_IDS))
        for record in records:
            record.category_item_id = atm_category_item.id
            record_repo.update(record)
