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
    from app.models.payable import Payable
    from app.models.payment import Payment
    from app.models.permission import Permission
    from app.models.purchase import Purchase
    from app.models.purchase_return import PurchaseReturn
    from app.models.receivable import Receivable
    from app.models.role import Role
    from app.models.sale import Sale
    from app.models.sale_return import SaleReturn
    from app.models.stock_adjustment import StockAdjustment
    from app.models.stock_transfer import StockTransfer
    from app.models.store import Store
    from app.models.supplier import Supplier
    from app.models.user_role import UserRole


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

    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    item_categories: list["ItemCategory"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    item_units: list["ItemUnit"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    stores: list["Store"] = Relationship(back_populates="owner", cascade_delete=True)
    suppliers: list["Supplier"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    customer_types: list["CustomerType"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    customers: list["Customer"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    purchases: list["Purchase"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    sales: list["Sale"] = Relationship(back_populates="owner", cascade_delete=True)
    accounts: list["Account"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    account_transactions: list["AccountTransaction"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    payments: list["Payment"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    stock_adjustments: list["StockAdjustment"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    stock_transfers: list["StockTransfer"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    payables: list["Payable"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    receivables: list["Receivable"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    sale_returns: list["SaleReturn"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    purchase_returns: list["PurchaseReturn"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    roles_owner: list["Role"] = Relationship(
        back_populates="owner",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Role.owner_id"},
    )
    roles_editor: list["Role"] = Relationship(
        back_populates="editor",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Role.editor_id"},
    )
    permissions_owner: list["Permission"] = Relationship(
        back_populates="owner",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Permission.owner_id"},
    )
    permissions_editor: list["Permission"] = Relationship(
        back_populates="editor",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Permission.editor_id"},
    )
    user_role: list["UserRole"] = Relationship(
        back_populates="user", cascade_delete=True
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
