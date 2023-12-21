from datetime import datetime, timedelta

from src.dusa_backend.domain.locations.repository import LocationRepository
from tests.factories.locations import LocationFactory


def test_create_record_created(client, db):
    assert not LocationRepository(db_session=db).exists()

    r = client.post("/location", json={"latitude": 45.0, "longitude": 45.0})
    assert r.status_code == 201
    assert r.json() == {"message": "Location created"}
    assert LocationRepository(db_session=db).exists()


def test_get_locations_no_locations_exist(client, db):
    r = client.get("/location/list")
    assert r.status_code == 200
    assert r.json() == {"locations": []}


def test_get_locations_correct(client, db):
    location1 = LocationFactory()
    location2 = LocationFactory()
    r = client.get("/location/list")
    assert r.status_code == 200
    assert r.json() == {
        "locations": [
            {"latitude": str(location1.latitude), "longitude": str(location1.longitude)},
            {"latitude": str(location2.latitude), "longitude": str(location2.longitude)},
        ]
    }


def test_get_locations_with_time_range_filter(client, db):
    location1 = LocationFactory()
    location2 = LocationFactory()
    location3 = LocationFactory(created=datetime.utcnow() - timedelta(days=1))
    r = client.get("/location/list?time_range=today")
    assert r.status_code == 200
    assert r.json() == {
        "locations": [
            {"latitude": str(location1.latitude), "longitude": str(location1.longitude)},
            {"latitude": str(location2.latitude), "longitude": str(location2.longitude)},
        ]
    }

    r = client.get("/location/list?time_range=yesterday")
    assert r.status_code == 200
    assert r.json() == {"locations": [{"latitude": str(location3.latitude), "longitude": str(location3.longitude)}]}

    r = client.get("/location/list?time_range=all_time")
    assert r.status_code == 200
    assert r.json() == {
        "locations": [
            {"latitude": str(location3.latitude), "longitude": str(location3.longitude)},
            {"latitude": str(location1.latitude), "longitude": str(location1.longitude)},
            {"latitude": str(location2.latitude), "longitude": str(location2.longitude)},
        ]
    }


def test_most_recent_location_none_exist(client, db):
    r = client.get("/location/recent")
    assert r.status_code == 200
    assert r.json() == {}


def test_most_recent_location_correct(client, db):
    LocationFactory()
    LocationFactory(created=datetime.utcnow() - timedelta(days=1))
    location3 = LocationFactory(created=datetime.utcnow() + timedelta(days=1))
    r = client.get("/location/recent")
    assert r.status_code == 200
    assert r.json() == {
        "id": str(location3.id),
        "created": location3.created.isoformat(),
        "latitude": str(location3.latitude),
        "longitude": str(location3.longitude),
    }
