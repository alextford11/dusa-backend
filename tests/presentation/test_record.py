import uuid

from src.dusa_backend.domain.records.repository import RecordRepository
from tests.factories.category_items import CategoryItemFactory


def test_create_record_category_item_not_found(client, db):
    r = client.post("/record/create", json={"category_item_id": str(uuid.uuid4()), "value": "12.34"})
    assert r.status_code == 404
    assert r.json() == {"detail": "CategoryItemTable not found"}


def test_create_record_item_created(client, db):
    assert not RecordRepository(db_session=db).exists()

    category_item = CategoryItemFactory()
    r = client.post("/record/create", json={"category_item_id": str(category_item.id), "value": "12.34"})
    assert r.status_code == 201
    assert r.json() == {"message": "Record created"}
    assert RecordRepository(db_session=db).exists()
