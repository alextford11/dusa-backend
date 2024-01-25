import uuid
from datetime import datetime

from dirty_equals import IsNow

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


def test_create_record_created_datetime(client, db):
    assert not RecordRepository(db_session=db).exists()

    category_item = CategoryItemFactory()
    r = client.post("/record", json={"category_item_id": str(category_item.id), "value": "12.34"})
    assert r.status_code == 201
    assert r.json() == {"message": "Record created"}
    assert RecordRepository(db_session=db).all()[0].created == IsNow

    created = datetime(2024, 1, 1)
    r = client.post(
        "/record", json={"category_item_id": str(category_item.id), "value": "12.34", "created": created.isoformat()}
    )
    assert r.status_code == 201
    assert r.json() == {"message": "Record created"}
    assert RecordRepository(db_session=db).all()[1].created == created


def test_get_records_list_empty(client, db):
    assert not RecordRepository(db_session=db).exists()

    r = client.get("/record")
    assert r.status_code == 200
    assert r.json() == {"records": []}


def test_get_records(client, db):
    record1 = RecordFactory()
    record2 = RecordFactory()
    r = client.get("/record")
    assert r.status_code == 200
    assert r.json() == {
        "records": [
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
    }

    for _ in range(15):
        RecordFactory()

    r = client.get("/record")
    assert r.status_code == 200
    assert len(r.json()["records"]) == 10

    for record in r.json()["records"]:
        assert str(record1.id) != record["id"]
        assert str(record2.id) != record["id"]
