import uuid

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.domain.records.repository import RecordRepository
from tests.factories.categories import CategoryFactory
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


def test_get_categories_no_categories(client, db):
    r = client.get("/category")
    assert r.status_code == 200
    assert r.json() == {"categories": []}


def test_get_categories_list_with_categories(client, db):
    record1 = RecordFactory()
    record2 = RecordFactory()
    r = client.get("/category/")
    assert r.status_code == 200
    assert r.json() == {
        "categories": [
            {
                "id": str(record1.category_item.category.id),
                "name": record1.category_item.category.name,
                "nsfw": False,
                "category_items": [
                    {
                        "id": str(record1.category_item.id),
                        "name": record1.category_item.name,
                        "records": [
                            {
                                "id": str(record1.id),
                                "created": record1.created.isoformat(),
                                "value": str(record1.value),
                            }
                        ],
                    }
                ],
            },
            {
                "id": str(record2.category_item.category.id),
                "name": record2.category_item.category.name,
                "nsfw": False,
                "category_items": [
                    {
                        "id": str(record2.category_item.id),
                        "name": record2.category_item.name,
                        "records": [
                            {
                                "id": str(record2.id),
                                "created": record2.created.isoformat(),
                                "value": str(record2.value),
                            }
                        ],
                    }
                ],
            },
        ]
    }


def test_update_category_not_found(client, db):
    r = client.post(f"/category/{uuid.uuid4()}", json={"name": "testing", "nsfw": False})
    assert r.status_code == 404


def test_update_category_updated(client, db):
    category = CategoryFactory(name="Test Category", nsfw=False)
    r = client.post(f"/category/{category.id}", json={"name": "testing", "nsfw": True})
    assert r.status_code == 200
    assert r.json() == {"message": "Category updated"}

    db.refresh(category)
    assert category.name == "testing"
    assert category.nsfw
