import uuid
from datetime import datetime

from sqlmodel import Field

from app.models import BaseModel


# Shared properties
class PermissionBase(BaseModel):
    name: str = Field(unique=True, index=True, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    pass


# Properties to receive via API on update, all are optional
class PermissionUpdate(PermissionBase):
    name: str | None = Field(unique=True, index=True, max_length=255)  # type: ignore


# Properties to return via API, id is always required
class PermissionPublic(PermissionBase):
    id: uuid.UUID
    date_created: datetime
    date_updated: datetime
    owner_id: uuid.UUID
    editor_id: uuid.UUID


class PermissionsPublic(BaseModel):
    data: list[PermissionPublic]
    count: int
