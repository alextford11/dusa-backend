import uuid
from datetime import datetime
from decimal import Decimal
from typing import Union

from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

MODELS = Union["CategoryTable", "CategoryItemTable", "RecordTable", "LocationTable"]


class CreatedTimestampMixin:
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)


class CategoryTable(Base):
    __tablename__ = "categories"

    name: Mapped[str]

    category_items = relationship("CategoryItemTable", back_populates="category")


class CategoryItemTable(Base):
    __tablename__ = "category_items"

    name: Mapped[str]
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"))

    category = relationship(CategoryTable, back_populates="category_items")
    records = relationship("RecordTable", back_populates="category_item")

    @property
    def records_value_sum(self):
        return sum(record.value for record in self.records)


class RecordTable(CreatedTimestampMixin, Base):
    __tablename__ = "records"

    value: Mapped[Decimal]
    nsfw: Mapped[bool] = mapped_column(default=False)
    category_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("category_items.id"))

    category_item = relationship(CategoryItemTable, back_populates="records")


class LocationTable(CreatedTimestampMixin, Base):
    __tablename__ = "locations"

    longitude: Mapped[Decimal]
    latitude: Mapped[Decimal]
