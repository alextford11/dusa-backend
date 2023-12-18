from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from tests.factories.categories import CategoryFactory
from tests.factories.category_items import CategoryItemFactory


def test_create_category_item_already_exists(client, db):
    category_item = CategoryItemFactory(name="testing")
    r = client.post("/category_item/create", json={"name": "testing", "category_id": str(category_item.category_id)})
    assert r.status_code == 400
    assert r.json() == {"detail": "Category Item already exists"}


def test_create_category_item_created(client, db):
    category = CategoryFactory()
    assert not CategoryItemRepository(db_session=db).exists()

    r = client.post("/category_item/create", json={"name": "testing", "category_id": str(category.id)})
    assert r.status_code == 201
    assert r.json() == {"message": "Category Item created"}
    assert CategoryItemRepository(db_session=db).exists()
