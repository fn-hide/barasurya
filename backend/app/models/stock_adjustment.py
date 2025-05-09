import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.user import User


class StockAdjustmentBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    type: str
    description: str | None = Field(default=None, max_length=255)
    date_adjustment: datetime


class StockAdjustmentCreate(StockAdjustmentBase):
    pass


class StockAdjustment(StockAdjustmentBase, table=True):
    __tablename__ = "stock_adjustment"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="stock_adjustments")
    item: "Item" = Relationship(back_populates="stock_adjustments")


class StockAdjustmentPublic(StockAdjustmentBase):
    id: uuid.UUID
    date_created: datetime
    owner_id: uuid.UUID
    item_id: uuid.UUID


class StockAdjustmentsPublic(BaseModel):
    data: list[StockAdjustmentPublic]
    count: int
