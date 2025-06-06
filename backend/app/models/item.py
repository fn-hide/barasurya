import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item_category import ItemCategory
    from app.models.item_unit import ItemUnit
    from app.models.purchase_item import PurchaseItem
    from app.models.purchase_return_item import PurchaseReturnItem
    from app.models.sale_item import SaleItem
    from app.models.sale_return_item import SaleReturnItem
    from app.models.stock_adjustment import StockAdjustment
    from app.models.stock_transfer import StockTransfer
    from app.models.user import User


# Shared properties
class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    price_purchase: float | None = None
    price_sell: float | None = None
    stock: int = Field(default=0, ge=0)  # ge=0 prevent stock to be negative
    stock_minimum: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    location: str | None = Field(default=None, max_length=50)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    item_category_id: uuid.UUID
    item_unit_id: uuid.UUID


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    item_category_id: uuid.UUID | None = Field(default=None)
    item_unit_id: uuid.UUID | None = Field(default=None)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    item_category_id: uuid.UUID = Field(
        foreign_key="item_category.id", nullable=False, ondelete="CASCADE"
    )
    item_unit_id: uuid.UUID = Field(
        foreign_key="item_unit.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="items")
    item_category: "ItemCategory" = Relationship(back_populates="items")
    item_unit: "ItemUnit" = Relationship(back_populates="items")
    purchase_items: list["PurchaseItem"] = Relationship(
        back_populates="item", cascade_delete=True
    )
    sale_items: list["SaleItem"] = Relationship(
        back_populates="item", cascade_delete=True
    )
    stock_adjustments: list["StockAdjustment"] = Relationship(
        back_populates="item", cascade_delete=True
    )
    stock_transfers: list["StockTransfer"] = Relationship(
        back_populates="item", cascade_delete=True
    )
    sale_return_items: list["SaleReturnItem"] = Relationship(
        back_populates="item", cascade_delete=True
    )
    purchase_return_items: list["PurchaseReturnItem"] = Relationship(
        back_populates="item", cascade_delete=True
    )


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    item_category_id: uuid.UUID
    item_unit_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
