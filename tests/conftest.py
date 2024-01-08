import pytest
from starlette.testclient import TestClient

from src.dusa_backend.infrastructure.database.session import get_engine
from src.dusa_backend.infrastructure.database.tables import Base
from src.dusa_backend.main import app
from tests.factories.base import TestSession


@pytest.fixture(name="client")
def get_client():
    with TestClient(app) as cli:
        return cli


@pytest.fixture(scope="session")
def engine():
    return get_engine()


@pytest.fixture(scope="function", autouse=True)
def initialize_db(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db():
    session = TestSession()
    yield session
    session.rollback()
    session.close()
