import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.account_transaction import AccountTransaction
    from app.models.customer import Customer
    from app.models.customer_type import CustomerType
    from app.models.item import Item
    from app.models.item_category import ItemCategory
    from app.models.item_unit import ItemUnit
    from app.models.payment import Payment
    from app.models.purchase import Purchase
    from app.models.sale import Sale
    from app.models.store import Store
    from app.models.supplier import Supplier


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

    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)  # type: ignore
    item_categories: list["ItemCategory"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    item_units: list["ItemUnit"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    stores: list["Store"] = Relationship(back_populates="owner", cascade_delete=True)  # type: ignore
    suppliers: list["Supplier"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    customer_types: list["CustomerType"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    customers: list["Customer"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    purchases: list["Purchase"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    sales: list["Sale"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    accounts: list["Account"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    account_transactions: list["AccountTransaction"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )
    payments: list["Payment"] = Relationship(  # type: ignore
        back_populates="owner", cascade_delete=True
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
