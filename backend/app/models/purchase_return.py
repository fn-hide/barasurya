import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.purchase import Purchase
    from app.models.supplier import Supplier
    from app.models.user import User


class PurchaseReturnBase(BaseModel):
    date_return: datetime
    amount: float = Field(default=0, ge=0)
    description: str | None = Field(default=None, max_length=255)


class PurchaseReturnCreate(PurchaseReturnBase):
    pass


class PurchaseReturnUpdate(PurchaseReturnBase):
    date_return: datetime | None = Field(default=0)  # type: ignore
    amount: float | None = Field(default=0, ge=0)  # type: ignore


class PurchaseReturn(PurchaseReturnBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    supplier_id: uuid.UUID = Field(
        foreign_key="supplier.id", nullable=False, ondelete="CASCADE"
    )
    purchase_id: uuid.UUID = Field(
        foreign_key="purchase.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="purchase_returns")
    supplier: "Supplier" = Relationship(back_populates="purchase_returns")
    purchase: "Purchase" = Relationship(back_populates="purchase_returns")


class PurchaseReturnPublic(PurchaseReturnBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    supplier_id: uuid.UUID
    purchase_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class PurchaseReturnsPublic(BaseModel):
    data: list[PurchaseReturnPublic]
    count: int
