import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.user import User


class CustomerTypeBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class CustomerTypeCreate(CustomerTypeBase):
    pass


class CustomerTypeUpdate(CustomerTypeBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class CustomerType(CustomerTypeBase, table=True):
    __tablename__ = "customer_type"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="customer_types")
    customers: list["Customer"] = Relationship(
        back_populates="customer_type", cascade_delete=True
    )


class CustomerTypePublic(CustomerTypeBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class CustomerTypesPublic(BaseModel):
    data: list[CustomerTypePublic]
    count: int
