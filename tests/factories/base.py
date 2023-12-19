from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import scoped_session

from src.dusa_backend.infrastructure.database.session import SessionLocal

TestSession = scoped_session(SessionLocal)


class FactoryBase(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = TestSession
        sqlalchemy_session_persistence = "commit"
