import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.account_transaction import AccountTransaction
    from app.models.user import User


class AccountBase(BaseModel):
    # TODO: add reference to "source" (bank, e-wallet, or anything account detail) if the app going bigger
    name: str = Field(min_length=1, max_length=100)
    balance: float = Field(default=0, ge=0)
    description: str | None = Field(default=None, max_length=255)


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    balance: float | None = Field(default=0, ge=0)


class Account(AccountBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="accounts")  # type: ignore
    account_transactions: list["AccountTransaction"] = Relationship(
        back_populates="account"
    )  # type: ignore


class AccountPublic(AccountBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class AccountsPublic(BaseModel):
    data: list[AccountPublic]
    count: int
