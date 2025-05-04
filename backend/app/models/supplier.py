import uuid
from datetime import datetime
from sqlmodel import Field, Relationship

from app.utils import utcnow
from app.models import BaseModel


class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SupplierBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class Supplier(SupplierBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="stores") # type: ignore
    

class SupplierPublic(SupplierBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class SuppliersPublic(BaseModel):
    data: list[SupplierPublic]
    count: int
