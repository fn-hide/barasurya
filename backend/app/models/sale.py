import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.sale_item import SaleItem
    from app.models.store import Store
    from app.models.user import User


class SaleBase(BaseModel):
    date_sale: datetime
    amount: float = Field(default=0, ge=0)
    description: str | None = Field(default=None, max_length=255)


class SaleCreate(SaleBase):
    pass


class SaleUpdate(SaleBase):
    date_sale: datetime | None = Field(default=0)  # type: ignore
    amount: float | None = Field(default=0, ge=0)  # type: ignore


class Sale(SaleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    customer_id: uuid.UUID = Field(
        foreign_key="customer.id", nullable=False, ondelete="CASCADE"
    )
    store_id: uuid.UUID = Field(
        foreign_key="store.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="sales")
    customer: "Customer" = Relationship(back_populates="sales")
    store: "Store" = Relationship(back_populates="sales")
    sale_items: list["SaleItem"] = Relationship(
        back_populates="sale", cascade_delete=True
    )


class SalePublic(SaleBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    customer_id: uuid.UUID
    store_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class SalesPublic(BaseModel):
    data: list[SalePublic]
    count: int
