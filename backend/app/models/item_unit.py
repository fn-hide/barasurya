import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.user import User


class ItemUnitBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class ItemUnitCreate(ItemUnitBase):
    pass


class ItemUnitUpdate(ItemUnitBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class ItemUnit(ItemUnitBase, table=True):
    __tablename__ = "item_unit"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="item_units")  # type: ignore

    item: "Item" = Relationship(back_populates="item_unit", cascade_delete=True)  # type: ignore


class ItemUnitPublic(ItemUnitBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemUnitsPublic(BaseModel):
    data: list[ItemUnitPublic]
    count: int
