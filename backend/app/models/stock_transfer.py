import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.store import Store
    from app.models.user import User


class StockTransferBase(BaseModel):
    quantity: int = Field(default=0, ge=0)
    type: str
    description: str | None = Field(default=None, max_length=255)
    date_transfer: datetime


class StockTransferCreate(StockTransferBase):
    pass


class StockTransfer(StockTransferBase, table=True):
    __tablename__ = "stock_transfer"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    item_id: uuid.UUID = Field(
        foreign_key="item.id", nullable=False, ondelete="CASCADE"
    )
    src_store_id: uuid.UUID = Field(
        foreign_key="store.id", nullable=False, ondelete="CASCADE"
    )
    dst_store_id: uuid.UUID = Field(
        foreign_key="store.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="stock_transfers")
    item: "Item" = Relationship(back_populates="stock_transfers")
    src_store: "Store" = Relationship(back_populates="src_stock_transfers")
    dst_store: "Store" = Relationship(back_populates="dst_stock_transfers")


class StockTransferPublic(StockTransferBase):
    id: uuid.UUID
    date_created: datetime
    owner_id: uuid.UUID
    item_id: uuid.UUID
    src_store_id: uuid.UUID
    dst_store_id: uuid.UUID


class StockTransfersPublic(BaseModel):
    data: list[StockTransferPublic]
    count: int
