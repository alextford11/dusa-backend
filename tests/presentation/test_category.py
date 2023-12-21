import uuid

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.domain.records.repository import RecordRepository
from tests.factories.categories import CategoryFactory
from tests.factories.category_items import CategoryItemFactory
from tests.factories.records import RecordFactory


def test_create_category_already_exists(client, db):
    CategoryFactory(name="testing")
    r = client.post("/category", json={"name": "testing", "nsfw": False})
    assert r.status_code == 400
    assert r.json() == {"detail": "Category already exists"}


def test_create_category_created(client, db):
    assert not CategoryRepository(db_session=db).exists()

    r = client.post("/category", json={"name": "testing", "nsfw": False})
    assert r.status_code == 201
    assert r.json() == {"message": "Category created"}

    category = CategoryRepository(db_session=db).all()[0]
    assert category.name == "testing"
    assert not category.nsfw


def test_create_category_created_with_nsfw(client, db):
    assert not CategoryRepository(db_session=db).exists()

    r = client.post("/category", json={"name": "testing", "nsfw": True})
    assert r.status_code == 201
    assert r.json() == {"message": "Category created"}

    category = CategoryRepository(db_session=db).all()[0]
    assert category.name == "testing"
    assert category.nsfw


def test_delete_category_404(client, db):
    r = client.delete(f"/category/{uuid.uuid4()}")
    assert r.status_code == 404
    assert r.json() == {"detail": "CategoryTable not found"}


def test_delete_category_deleted(client, db):
    category = CategoryFactory()
    r = client.delete(f"/category/{category.id}")
    assert r.status_code == 200
    assert r.json() == {"message": "Category deleted"}
    assert not CategoryRepository(db_session=db).exists()


def test_delete_category_with_category_items_and_records(client, db):
    record = RecordFactory()
    r = client.delete(f"/category/{record.category_item.category.id}")
    assert r.status_code == 200
    assert r.json() == {"message": "Category deleted"}
    assert not CategoryRepository(db_session=db).exists()
    assert not CategoryItemRepository(db_session=db).exists()
    assert not RecordRepository(db_session=db).exists()
