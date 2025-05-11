import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User


# Shared properties
class UserRoleBase(BaseModel):
    pass


# Properties to receive via API on creation
class UserRoleCreate(UserRoleBase):
    pass


# Properties to receive via API on update, all are optional
class UserRoleUpdate(UserRoleBase):
    pass


# Database model, database table inferred from class name
class UserRole(UserRoleBase, table=True):
    __tablename__ = "user_role"

    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", primary_key=True, nullable=False, ondelete="CASCADE"
    )
    role_id: uuid.UUID = Field(
        foreign_key="role.id", primary_key=True, nullable=False, ondelete="CASCADE"
    )

    user: "User" = Relationship(back_populates="user_role")
    role: "Role" = Relationship(back_populates="user_role")


# Properties to return via API, id is always required
class UserRolePublic(UserRoleBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime
    user_id: uuid.UUID
    role_id: uuid.UUID


class UserRolesPublic(BaseModel):
    data: list[UserRolePublic]
    count: int
