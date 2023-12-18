from typing import List, Any, Union

from fastapi import Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


from src.dusa_backend.infrastructure.database.tables import Base


class BaseRepository:
    model: Any | BaseModel = NotImplemented

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get(self, **kwargs) -> Row:
        return self.db_session.query(self.model).filter_by(**kwargs).one()

    def filter(self, *args, **kwargs) -> Query:
        q = self.db_session.query(self.model)
        if args:
            q = q.filter(*args)
        if kwargs:
            q = q.filter_by(**kwargs)
        return q

    def all(self) -> list[Row]:
        return self.db_session.query(self.model).all()

    def count(self, **kwargs) -> int:
        return self.db_session.query(self.model).filter_by(**kwargs).count()

    def create(self, instance: Base) -> Base:
        assert not instance.id

        if hasattr(instance, "pre_create"):
            instance.pre_create(db=self.db_session)
        try:
            self.db_session.add(instance)
            self.db_session.commit()
            self.db_session.flush()
        except IntegrityError:
            self.db_session.rollback()
            self.update(instance)

        if hasattr(instance, "post_create"):
            instance.post_create(db=self.db_session)
        return instance

    def update(self, instance: Base) -> Base:
        assert instance.id

        try:
            self.merge(instance)
        except IntegrityError:
            self.db_session.rollback()
        else:
            self.db_session.commit()
            self.db_session.flush()
        return instance

    def merge(self, instance):
        self.db_session.merge(instance)
        self.db_session.commit()
        self.db_session.flush()

    def get_or_create(self, **kwargs) -> tuple[Row, bool]:
        created = False
        try:
            instance = self.get(**kwargs)
        except NoResultFound:
            instance = self.create(self.model(**kwargs))
            created = True
        return instance, created

    def create_or_update(self, instance: Base) -> Base:
        if instance.id:
            return self.update(instance)
        return self.create(instance)

    def delete(self, *args, **kwargs) -> int:
        count = self.db_session.query(self.model).filter(*args).filter_by(**kwargs).delete()
        self.db_session.commit()
        self.db_session.flush()
        return count

    def create_many(self, *instances: list[Base]) -> None:
        self.db_session.add_all(*instances)
        self.db_session.commit()

    def exists(self, **kwargs) -> bool:
        return bool(self.db_session.query(self.model).filter_by(**kwargs).first())

    def order_by(self, *args) -> Query:
        return self.db_session.query(self.model).order_by(*args)


def get_object_or_404(db_session: Session, model: Any, **kwargs) -> Row:
    try:
        obj = db_session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    else:
        return obj
