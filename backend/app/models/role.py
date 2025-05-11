import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.role_permission import RolePermission
    from app.models.user import User
    from app.models.user_role import UserRole


# Shared properties
class RoleBase(BaseModel):
    name: str = Field(unique=True, index=True, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update, all are optional
class RoleUpdate(RoleBase):
    name: str | None = Field(unique=True, index=True, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Role(RoleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    editor_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )

    owner: "User" = Relationship(back_populates="roles_owner")
    editor: "User" = Relationship(back_populates="roles_editor")
    user_role: "UserRole" = Relationship(back_populates="role")
    role_permission: "RolePermission" = Relationship(back_populates="role")


# Properties to return via API, id is always required
class RolePublic(RoleBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime
    owner_id: uuid.UUID
    editor_id: uuid.UUID


class RolesPublic(BaseModel):
    data: list[RolePublic]
    count: int
