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


class PaymentMethod(str, Enum):
    cash = "cash"
    transfer = "transfer"


class PaymentBase(BaseModel):
    date_payment: datetime
    amount: float = Field(default=0, ge=0)
    method: PaymentMethod
    reference_id: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    transaction_type: str | None = Field(default=None, max_length=255)
    transaction_id: uuid.UUID | None = Field(default=None)
    subject_type: str | None = Field(default=None, max_length=255)
    subject_id: uuid.UUID | None = Field(default=None)
    is_reversal: bool = Field(default=False)
    is_reversal_payment_id: uuid.UUID | None = Field(default=None)


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    account_id: uuid.UUID = Field(
        foreign_key="account.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="payments")
    account: "Account" = Relationship(back_populates="payments")


class PaymentPublic(PaymentBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    account_id: uuid.UUID
    date_created: datetime


class PaymentsPublic(BaseModel):
    data: list[PaymentPublic]
    count: int
