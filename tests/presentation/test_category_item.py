import uuid

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.domain.records.repository import RecordRepository
from tests.factories.categories import CategoryFactory
from tests.factories.category_items import CategoryItemFactory
from tests.factories.records import RecordFactory


def test_create_category_item_already_exists(client, db):
    category_item = CategoryItemFactory(name="testing")
    r = client.post("/category_item", json={"name": "testing", "category_id": str(category_item.category_id)})
    assert r.status_code == 400
    assert r.json() == {"detail": "Category Item already exists"}


def test_create_category_item_created(client, db):
    category = CategoryFactory()
    assert not CategoryItemRepository(db_session=db).exists()

    r = client.post("/category_item", json={"name": "testing", "category_id": str(category.id)})
    assert r.status_code == 201
    assert r.json() == {"message": "Category Item created"}
    assert CategoryItemRepository(db_session=db).exists()


def test_delete_category_item_404(client, db):
    r = client.delete(f"/category_item/{uuid.uuid4()}")
    assert r.status_code == 404
    assert r.json() == {"detail": "CategoryItemTable not found"}


def test_delete_category_item_deleted(client, db):
    category_item = CategoryItemFactory()
    r = client.delete(f"/category_item/{category_item.id}")
    assert r.status_code == 200
    assert r.json() == {"message": "Category Item deleted"}
    assert not CategoryItemRepository(db_session=db).exists()


def test_delete_category_item_with_records(client, db):
    record = RecordFactory()
    r = client.delete(f"/category_item/{record.category_item.id}")
    assert r.status_code == 200
    assert r.json() == {"message": "Category Item deleted"}
    assert CategoryRepository(db_session=db).exists()
    assert not CategoryItemRepository(db_session=db).exists()
    assert not RecordRepository(db_session=db).exists()
