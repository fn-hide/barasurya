import uuid
from datetime import datetime
from sqlmodel import Field, Relationship

from app.utils import utcnow
from app.models import BaseModel


class StoreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str | None = Field(default=None, max_length=255)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)


class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class Store(StoreBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="stores") # type: ignore
    

class StorePublic(StoreBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class StoresPublic(BaseModel):
    data: list[StorePublic]
    count: int
