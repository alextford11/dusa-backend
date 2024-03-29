from dusa_backend.domain.records.repository import RecordRepository
from dusa_backend.infrastructure.database.session import SessionLocal

RECORD_IDS_TO_DELETE = ["59ee22e2-3e8f-4e4e-94b8-5f7bb78e1482", "147c52ba-e766-4c63-96b8-da51834f6528"]


def remove_records():
    count = 0
    with SessionLocal() as db_session:
        record_repo = RecordRepository(db_session)
        for record_id in RECORD_IDS_TO_DELETE:
            count += record_repo.delete(id=record_id)
    print(f"Removed {count} records")
