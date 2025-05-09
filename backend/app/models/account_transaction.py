import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.user import User


class AccountTransactionBase(BaseModel):
    type: str
    amount: float = Field(default=0, ge=0)
    # TODO: consider to add return transaction
    reference_name: str
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

    owner: "User" = Relationship(back_populates="account_transactions")
    account: "Account" = Relationship(back_populates="account_transactions")


class AccountTransactionPublic(AccountTransactionBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    date_created: datetime


class AccountTransactionsPublic(BaseModel):
    data: list[AccountTransactionPublic]
    count: int
