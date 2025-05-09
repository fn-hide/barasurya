import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.sale import Sale
    from app.models.user import User


class ReceivableBase(BaseModel):
    date_payable: datetime
    amount: float = Field(default=0, ge=0)
    amount_paid: float = Field(default=0, ge=0)
    status: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ReceivableCreate(ReceivableBase):
    pass


class ReceivableUpdate(ReceivableBase):
    date_payable: datetime | None = Field(default=0)  # type: ignore
    amount: float | None = Field(default=0, ge=0)  # type: ignore
    amount_paid: float | None = Field(default=0, ge=0)  # type: ignore


class Receivable(ReceivableBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    customer_id: uuid.UUID = Field(
        foreign_key="customer.id", nullable=False, ondelete="CASCADE"
    )
    sale_id: uuid.UUID = Field(
        foreign_key="sale.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="receivables")
    customer: "Customer" = Relationship(back_populates="receivables")
    sale: "Sale" = Relationship(back_populates="receivables")


class ReceivablePublic(ReceivableBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    customer_id: uuid.UUID
    sale_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ReceivablesPublic(BaseModel):
    data: list[ReceivablePublic]
    count: int
