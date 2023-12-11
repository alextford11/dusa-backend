import factory

from src.dusa_backend.infrastructure.database.tables import CategoryTable
from tests.factories.base import FactoryBase


class CategoryFactory(FactoryBase):
    class Meta:
        model = CategoryTable

    name = factory.Sequence(lambda n: f"Category{n}")
