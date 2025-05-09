import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.customer_type import CustomerType
    from app.models.receivable import Receivable
    from app.models.sale import Sale
    from app.models.user import User


class CustomerBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)


class CustomerCreate(CustomerBase):
    customer_type_id: uuid.UUID


class CustomerUpdate(CustomerBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    customer_type_id: uuid.UUID | None = Field(default=None)


class Customer(CustomerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    customer_type_id: uuid.UUID = Field(
        foreign_key="customer_type.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="customers")
    customer_type: "CustomerType" = Relationship(back_populates="customers")
    sales: list["Sale"] = Relationship(back_populates="customer", cascade_delete=True)
    receivables: list["Receivable"] = Relationship(
        back_populates="customer", cascade_delete=True
    )


class CustomerPublic(CustomerBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    customer_type_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class CustomersPublic(BaseModel):
    data: list[CustomerPublic]
    count: int
