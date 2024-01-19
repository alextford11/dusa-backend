from datetime import datetime

import factory

from src.dusa_backend.infrastructure.database.tables import RecordTable
from tests.factories.base import FactoryBase
from tests.factories.category_items import CategoryItemFactory


class RecordFactory(FactoryBase):
    class Meta:
        model = RecordTable

    value = factory.Faker("pyint", min_value=1, max_value=10)
    category_item = factory.SubFactory(CategoryItemFactory)
    created = factory.LazyFunction(datetime.utcnow)
