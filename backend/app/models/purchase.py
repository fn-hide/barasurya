import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.purchase_item import PurchaseItem
    from app.models.store import Store
    from app.models.supplier import Supplier
    from app.models.user import User


class PurchaseBase(BaseModel):
    date_purchase: datetime
    amount: float = Field(default=0, ge=0)
    description: str | None = Field(default=None, max_length=255)


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(PurchaseBase):
    date_purchase: datetime | None = Field(default=0)  # type: ignore
    amount: float | None = Field(default=0, ge=0)  # type: ignore


class Purchase(PurchaseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="purchase")  # type: ignore

    supplier_id: uuid.UUID = Field(
        foreign_key="supplier.id", nullable=False, ondelete="CASCADE"
    )
    supplier: "Supplier" = Relationship(back_populates="purchase", cascade_delete=True)  # type: ignore

    store_id: uuid.UUID = Field(
        foreign_key="store.id", nullable=False, ondelete="CASCADE"
    )
    store: "Store" = Relationship(back_populates="purchase", cascade_delete=True)  # type: ignore

    purchase_item: list["PurchaseItem"] = Relationship(  # type: ignore
        back_populates="purchase", cascade_delete=True
    )


class PurchasePublic(PurchaseBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    supplier_id: uuid.UUID
    store_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class PurchasesPublic(BaseModel):
    data: list[PurchasePublic]
    count: int
