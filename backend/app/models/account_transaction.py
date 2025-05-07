import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Literal

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.user import User


class AccountTransactionBase(BaseModel):
    type: Literal["income", "expense", "transfer_in", "transfer_out"]
    amount: float = Field(default=0, ge=0)
    reference_name: Literal["sale", "purchase"]
    reference_id: uuid.UUID
    description: str | None = Field(default=None, max_length=255)


class AccountTransactionCreate(AccountTransactionBase):
    pass


class AccountTransactionUpdate(AccountTransactionBase):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    balance: float | None = Field(default=0, ge=0)


class AccountTransaction(AccountTransactionBase, table=True):
    __tablename__ = "account_transactions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="accounts")  # type: ignore


class AccountTransactionPublic(AccountTransactionBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime
    date_updated: datetime


class AccountTransactionsPublic(BaseModel):
    data: list[AccountTransactionPublic]
    count: int
