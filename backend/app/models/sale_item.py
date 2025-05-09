import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.sale import Sale


class SaleItemBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(SaleItemBase):
    quantity: int | None = Field(default=0, ge=0)  # type: ignore
    price: float | None = Field(default=0, ge=0)  # type: ignore


class SaleItem(SaleItemBase, table=True):
    __tablename__ = "sale_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    sale_id: uuid.UUID = Field(
        foreign_key="sale.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )

    sale: "Sale" = Relationship(back_populates="sale_items")  # type: ignore
    item: "Item" = Relationship(back_populates="sale_items")  # type: ignore


class SaleItemPublic(SaleItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    sale_id: uuid.UUID
    item_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class SaleItemsPublic(BaseModel):
    data: list[SaleItemPublic]
    count: int
