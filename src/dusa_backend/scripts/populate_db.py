from random import randint, uniform

from src.dusa_backend.domain.categories.repository import CategoryRepository
from src.dusa_backend.domain.category_items.repository import CategoryItemRepository
from src.dusa_backend.domain.locations.repository import LocationRepository
from src.dusa_backend.domain.records.repository import RecordRepository
from src.dusa_backend.infrastructure.database.session import get_db, SessionLocal
from src.dusa_backend.infrastructure.database.tables import CategoryTable, CategoryItemTable, RecordTable, LocationTable

CATEGORIES_AND_ITEMS = (
    ("Drinks", ["Shots", "Beers", "Whiskeys", "G&Ts"], True),
    ("Walking", ["Steps", "Kilometers Walked", "Flights Climbed"], False),
    ("Activities", ["Surfed", "Walked", "Skydived"], False),
)
LOCATION_COORDS = [
    (-33.932016, 151.173380),
    (-33.856351, 151.204470),
    (-33.801993, 151.290254),
    (-33.833101, 151.217459),
    (-33.801993, 151.290254),
    (-33.880110, 151.191796),
    (-28.648615, 153.615486),
    (-28.639942, 153.610264),
    (-28.648971, 153.617899),
    (-27.996182, 153.427205),
    (-28.017067, 153.433783),
    (-27.996182, 153.427205),
    (-27.465456, 153.028686),
    (-27.479283, 153.029323),
    (-27.465456, 153.028686),
    (-26.400025, 153.064517),
    (-26.405295, 153.107149),
    (-26.400025, 153.064517),
    (-26.406164, 153.087361),
    (-26.400025, 153.064517),
]


def populate_db():
    print("Populating database...")
    with SessionLocal() as db_session:
        category_repo = CategoryRepository(db_session)
        category_item_repo = CategoryItemRepository(db_session)
        record_repo = RecordRepository(db_session)
        for category_name, category_item_names, nsfw in CATEGORIES_AND_ITEMS:
            category = category_repo.create(CategoryTable(name=category_name, nsfw=nsfw))
            for category_item_name in category_item_names:
                category_item = category_item_repo.create(CategoryItemTable(name=category_item_name, category=category))
                for _ in range(1, randint(2, 5)):
                    record_repo.create(RecordTable(category_item=category_item, value=round(uniform(1, 5), 1)))

        location_repo = LocationRepository(db_session)
        for longitude, latitude in LOCATION_COORDS:
            location_repo.create(LocationTable(longitude=longitude, latitude=latitude))
    print("Populated!")


if __name__ == "__main__":
    populate_db()
