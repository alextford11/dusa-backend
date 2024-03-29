from typing import Callable, Generator

from google.cloud.sql.connector import Connector
from sqlalchemy import Engine, create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.dusa_backend.core.settings import settings


def get_engine() -> Engine:
    """
    Returns a SQLAlchemy engine instance.
    """
    if settings.is_testing or settings.is_local:
        return create_engine(settings.db_uri)
    else:
        return get_cloud_sql_engine()


def get_cloud_sql_engine() -> Engine:  # pragma: no cover
    """
    Create and return an engine for the Cloud SQL connection.

    :return: Returns an Engine instance for the Cloud SQL connection.
    """
    connector = Connector()

    def get_cloud_sql_connection() -> Connection:
        """
        Gets a Google Cloud SQL connection which can be used to connect to a Cloud SQL database.

        :return: Returns a pg8000 Connection instance for Google Cloud SQL.
        """
        return connector.connect(
            f"{settings.google_cloud_project}:{settings.google_cloud_region}:{settings.cloud_sql_instance}",
            "pg8000",
            user=settings.db_user,
            password=settings.db_password,
            db=settings.db_name,
        )

    return create_engine("postgresql+pg8000://", creator=get_cloud_sql_connection)


def get_session() -> Callable[..., Session]:
    """
    Returns a SQLAlchemy session instance.
    """
    engine = get_engine()
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session


SessionLocal = get_session()


def get_db() -> Generator[Session, None, None]:
    """
    Yields a SQLAlchemy session instance.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        # closes the session once finished with, instead of keeping it open
        db.close()
