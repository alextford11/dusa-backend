from src.dusa_backend.domain.categories.repository import CategoryRepository
from tests.factories.categories import CategoryFactory


def test_create_category_already_exists(client, db):
    CategoryFactory(name="testing")
    r = client.post("/category/create", json={"name": "testing"})
    assert r.status_code == 400
    assert r.json() == {"detail": "Category already exists"}


def test_create_category_created(client, db):
    assert not CategoryRepository(db_session=db).exists()

    r = client.post("/category/create", json={"name": "testing"})
    assert r.status_code == 201
    assert r.json() == {"message": "Category created"}
    assert CategoryRepository(db_session=db).exists()
