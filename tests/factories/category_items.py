import factory

from src.dusa_backend.infrastructure.database.tables import CategoryItemTable
from tests.factories.base import FactoryBase
from tests.factories.categories import CategoryFactory


class CategoryItemFactory(FactoryBase):
    class Meta:
        model = CategoryItemTable

    name = factory.Sequence(lambda n: f"CategoryItem{n}")
    category = factory.SubFactory(CategoryFactory)
