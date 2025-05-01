import uuid
from datetime import datetime
from sqlmodel import Field, Relationship

from app.utils import utcnow
from app.models import BaseModel


class ItemCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class ItemCategoryCreate(ItemCategoryBase):
    pass


class ItemCategoryUpdate(ItemCategoryBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class ItemCategory(ItemCategoryBase, table=True):
    __tablename__ = "item_category"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="item_categories")
    
    items: list["Item"] = Relationship(back_populates="item_category", cascade_delete=True)


class ItemCategoryPublic(ItemCategoryBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemCategoriesPublic(BaseModel):
    data: list[ItemCategoryPublic]
    count: int
