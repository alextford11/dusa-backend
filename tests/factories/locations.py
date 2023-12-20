import factory

from src.dusa_backend.infrastructure.database.tables import LocationTable
from tests.factories.base import FactoryBase


class LocationFactory(FactoryBase):
    class Meta:
        model = LocationTable

    latitude = factory.Faker("pyfloat", min_value=-180, max_value=180)
    longitude = factory.Faker("pyfloat", min_value=-90, max_value=90)
