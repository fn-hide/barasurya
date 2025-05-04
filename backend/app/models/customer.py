import uuid
from datetime import datetime
from sqlmodel import Field, Relationship

from app.utils import utcnow
from app.models import BaseModel


class CustomerBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class Customer(CustomerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="customers") # type: ignore
    
    customer_type_id: uuid.UUID = Field(
        foreign_key="customer_type.id", nullable=False, ondelete="CASCADE"
    )
    customer_type: "CustomerType" = Relationship(back_populates="customers") # type: ignore
    

class CustomerPublic(CustomerBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class CustomersPublic(BaseModel):
    data: list[CustomerPublic]
    count: int
