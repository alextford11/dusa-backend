import uuid

from src.dusa_backend.domain.categories.repository import CategoryRepository
from tests.factories.categories import CategoryFactory


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
    category = CategoryFactory(name="testing")
    r = client.delete(f"/category/{category.id}")
    assert r.status_code == 200
    assert r.json() == {"message": "Category deleted"}
    assert not CategoryRepository(db_session=db).exists()
