import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import BaseModel
from app.utils import utcnow

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.role import Role


# Shared properties
class RolePermissionBase(BaseModel):
    pass


# Properties to receive via API on creation
class RolePermissionCreate(RolePermissionBase):
    pass


# Properties to receive via API on update, all are optional
class RolePermissionUpdate(RolePermissionBase):
    pass


# Database model, database table inferred from class name
class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "role_permission"

    date_created: datetime = Field(default_factory=utcnow)
    date_updated: datetime = Field(default_factory=utcnow)
    role_id: uuid.UUID = Field(
        foreign_key="role.id", primary_key=True, nullable=False, ondelete="CASCADE"
    )
    permission_id: uuid.UUID = Field(
        foreign_key="permission.id",
        primary_key=True,
        nullable=False,
        ondelete="CASCADE",
    )

    role: "Role" = Relationship(back_populates="role_permission")
    permission: "Permission" = Relationship(back_populates="role_permission")


# Properties to return via API, id is always required
class RolePermissionPublic(RolePermissionBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime
    role_id: uuid.UUID
    permission_id: uuid.UUID


class RolePermissionsPublic(BaseModel):
    data: list[RolePermissionPublic]
    count: int
