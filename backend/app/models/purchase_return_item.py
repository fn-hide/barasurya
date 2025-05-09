import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.purchase_return import PurchaseReturn


class PurchaseReturnItemBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0)


class PurchaseReturnItemCreate(PurchaseReturnItemBase):
    pass


class PurchaseReturnItemUpdate(PurchaseReturnItemBase):
    quantity: int | None = Field(default=0, ge=0)  # type: ignore
    price: float | None = Field(default=0, ge=0)  # type: ignore


class PurchaseReturnItem(PurchaseReturnItemBase, table=True):
    __tablename__ = "purchase_return_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    purchase_return_id: uuid.UUID = Field(
        foreign_key="purchase_return.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )

    purchase_return: "PurchaseReturn" = Relationship(
        back_populates="purchase_return_items"
    )
    item: "Item" = Relationship(back_populates="purchase_return_items")


class PurchaseReturnItemPublic(PurchaseReturnItemBase):
    id: uuid.UUID
    purchase_return_id: uuid.UUID
    item_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class PurchaseReturnItemsPublic(BaseModel):
    data: list[PurchaseReturnItemPublic]
    count: int
