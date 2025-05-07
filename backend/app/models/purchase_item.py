import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.purchase import Purchase
    from app.models.user import User


class PurchaseItemBase(BaseModel):
    price: float = Field(default=0, ge=0)


class PurchaseItemCreate(PurchaseItemBase):
    pass


class PurchaseItemUpdate(PurchaseItemBase):
    price: float | None = Field(default=0, ge=0)  # type: ignore


class PurchaseItem(PurchaseItemBase, table=True):
    __tablename__ = "purchase_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    purchase_id: uuid.UUID = Field(
        foreign_key="purchase.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="purchase_items")  # type: ignore
    purchase: "Purchase" = Relationship(back_populates="purchase_items")  # type: ignore
    item: "Item" = Relationship(back_populates="purchase_items")  # type: ignore


class PurchaseItemPublic(PurchaseItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    purchase_id: uuid.UUID
    item_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class PurchaseItemsPublic(BaseModel):
    data: list[PurchaseItemPublic]
    count: int
