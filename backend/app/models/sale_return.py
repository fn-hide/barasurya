import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.sale import Sale
    from app.models.sale_return_item import SaleReturnItem
    from app.models.user import User


class SaleReturnBase(BaseModel):
    date_return: datetime
    amount: float = Field(default=0, ge=0)
    description: str | None = Field(default=None, max_length=255)


class SaleReturnCreate(SaleReturnBase):
    pass


class SaleReturnUpdate(SaleReturnBase):
    date_return: datetime | None = Field(default=0)  # type: ignore
    amount: float | None = Field(default=0, ge=0)  # type: ignore


class SaleReturn(SaleReturnBase, table=True):
    __tablename__ = "sale_return"

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

    owner: "User" = Relationship(back_populates="sale_returns")
    customer: "Customer" = Relationship(back_populates="sale_returns")
    sale: "Sale" = Relationship(back_populates="sale_returns")
    sale_return_items: list["SaleReturnItem"] = Relationship(
        back_populates="sale_return", cascade_delete=True
    )


class SaleReturnPublic(SaleReturnBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    customer_id: uuid.UUID
    sale_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class SaleReturnsPublic(BaseModel):
    data: list[SaleReturnPublic]
    count: int
