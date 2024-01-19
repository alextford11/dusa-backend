import uuid

from src.dusa_backend.domain.records.repository import RecordRepository
from tests.factories.category_items import CategoryItemFactory
from tests.factories.records import RecordFactory


def test_create_record_category_item_not_found(client, db):
    r = client.post("/record", json={"category_item_id": str(uuid.uuid4()), "value": "12.34"})
    assert r.status_code == 404
    assert r.json() == {"detail": "CategoryItemTable not found"}


def test_create_record_created(client, db):
    assert not RecordRepository(db_session=db).exists()

    category_item = CategoryItemFactory()
    r = client.post("/record", json={"category_item_id": str(category_item.id), "value": "12.34"})
    assert r.status_code == 201
    assert r.json() == {"message": "Record created"}
    assert RecordRepository(db_session=db).exists()


def test_get_records_list_empty(client, db):
    assert not RecordRepository(db_session=db).exists()

    r = client.get("/record")
    assert r.status_code == 200
    assert r.json() == []


def test_get_records(client, db):
    record1 = RecordFactory()
    record2 = RecordFactory()
    r = client.get("/record")
    assert r.status_code == 200
    assert r.json() == [
        {
            "id": str(record2.id),
            "value": str(record2.value),
            "created": record2.created.isoformat(),
            "category_item_name": record2.category_item.name,
            "category_name": record2.category_item.category.name,
        },
        {
            "id": str(record1.id),
            "value": str(record1.value),
            "created": record1.created.isoformat(),
            "category_item_name": record1.category_item.name,
            "category_name": record1.category_item.category.name,
        },
    ]

    for _ in range(15):
        RecordFactory()

    r = client.get("/record")
    assert r.status_code == 200
    assert len(r.json()) == 10

    for record in r.json():
        assert str(record1.id) != record["id"]
        assert str(record2.id) != record["id"]
