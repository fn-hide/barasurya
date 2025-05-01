import uuid
from datetime import datetime, timezone

from pydantic import EmailStr, ConfigDict
from sqlmodel import Field, Relationship, SQLModel


# a helper function to generate a datetime in utc
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# setup constraint naming convention, so we add flexibility to modify constraint later
# source: https://github.com/fastapi/sqlmodel/discussions/1213
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(SQLModel):
    """Base model for everything by add naming convention feature."""

    model_config = ConfigDict(
        protected_namespaces=(),
    )  # type: ignore


BaseModel.metadata.naming_convention = convention


class BaseModelUpdate(BaseModel):
    date_updated: datetime = Field(default_factory=utcnow)


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
    
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    item_categories: list["ItemCategory"] = Relationship(back_populates="owner", cascade_delete=True)
    item_units: list["ItemUnit"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


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
    owner: User | None = Relationship(back_populates="item_categories")
    
    items: list["Item"] = Relationship(back_populates="item_category", cascade_delete=True)


class ItemCategoryPublic(ItemCategoryBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemCategoriesPublic(BaseModel):
    data: list[ItemCategoryPublic]
    count: int


class ItemUnitBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class ItemUnitCreate(ItemUnitBase):
    pass


class ItemUnitUpdate(ItemUnitBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)


class ItemUnit(ItemUnitBase, table=True):
    __tablename__ = "item_unit"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="item_units")
    
    items: list["Item"] = Relationship(back_populates="item_unit", cascade_delete=True)


class ItemUnitPublic(ItemUnitBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemUnitsPublic(BaseModel):
    data: list[ItemUnitPublic]
    count: int


# Shared properties
class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    price_purchase: float | None = None
    price_sell: float | None = None
    stock: int = Field(default=0, ge=0)  # ge=0 prevent stock to be negative
    stock_minimum: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    location: str | None = Field(default=None, max_length=50)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    item_category_id: uuid.UUID


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")
    
    item_category_id: uuid.UUID = Field(
        foreign_key="item_category.id", nullable=False, ondelete="CASCADE"
    )
    item_category: ItemCategory | None = Relationship(back_populates="items")
    
    item_unit_id: uuid.UUID = Field(
        foreign_key="item_unit.id", nullable=False, ondelete="CASCADE"
    )
    item_unit: ItemUnit | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
