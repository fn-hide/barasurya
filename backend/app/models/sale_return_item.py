import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.sale_return import SaleReturn


class SaleReturnItemBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0)


class SaleReturnItemCreate(SaleReturnItemBase):
    pass


class SaleReturnItemUpdate(SaleReturnItemBase):
    quantity: int | None = Field(default=0, ge=0)  # type: ignore
    price: float | None = Field(default=0, ge=0)  # type: ignore


class SaleReturnItem(SaleReturnItemBase, table=True):
    __tablename__ = "sale_return_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    sale_return_id: uuid.UUID = Field(
        foreign_key="sale_return.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )

    sale_return: "SaleReturn" = Relationship(back_populates="sale_return_items")
    item: "Item" = Relationship(back_populates="sale_return_items")


class SaleReturnItemPublic(SaleReturnItemBase):
    id: uuid.UUID
    sale_return_id: uuid.UUID
    item_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class SaleReturnItemsPublic(BaseModel):
    data: list[SaleReturnItemPublic]
    count: int
