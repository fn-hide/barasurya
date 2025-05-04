import uuid
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.utils import utcnow
from app.models import BaseModel


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    item_categories: list["ItemCategory"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    item_units: list["ItemUnit"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    stores: list["Store"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    suppliers: list["Supplier"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    customer_types: list["CustomerType"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore
    customers: list["Customer"] = Relationship(back_populates="owner", cascade_delete=True) # type: ignore


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
