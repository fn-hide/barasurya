import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.user import User


class AccountTransactionType(str, Enum):
    income = "income"
    expense = "expense"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"


class ReferenceName(str, Enum):
    sale = "sale"
    purchase = "purchase"
    payable = "payable"
    receivable = "receivable"


class AccountTransactionBase(BaseModel):
    type: AccountTransactionType
    amount: float = Field(default=0, ge=0)
    # TODO: consider to add return transaction
    reference_name: ReferenceName
    reference_id: uuid.UUID
    description: str | None = Field(default=None, max_length=255)


class AccountTransactionCreate(AccountTransactionBase):
    pass


class AccountTransaction(AccountTransactionBase, table=True):
    __tablename__ = "account_transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    account_id: uuid.UUID = Field(
        foreign_key="account.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="account_transactions")  # type: ignore
    account: "Account" = Relationship(back_populates="account_transactions")  # type: ignore


class AccountTransactionPublic(AccountTransactionBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime


class AccountTransactionsPublic(BaseModel):
    data: list[AccountTransactionPublic]
    count: int
