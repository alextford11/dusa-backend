from typing import Callable, Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.dusa_backend.core.settings import settings


def get_engine() -> Engine:
    """
    Returns a SQLAlchemy engine instance.
    """
    return create_engine(settings.db_uri)


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
