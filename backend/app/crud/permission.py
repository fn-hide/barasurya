import uuid
from typing import Any

from fastapi import HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import (
    BaseModelUpdate,
    Message,
    Permission,
    PermissionCreate,
    PermissionsPublic,
    PermissionUpdate,
)


def get_permissions(session: SessionDep, skip=0, limit=10) -> Any:
    count_statement = select(func.count()).select_from(Permission)
    count = session.exec(count_statement).one()

    statement = select(Permission).offset(skip).limit(limit)
    permissions = session.exec(statement).all()

    return PermissionsPublic(data=permissions, count=count)


def get_permission(session: SessionDep, permission_id: uuid.UUID):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


def create_permission(session: SessionDep, permission_in: PermissionCreate) -> Any:
    permission = Permission.model_validate(permission_in)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


def update_permission(
    session: SessionDep, permission_id: int, permission_in: PermissionUpdate
):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    update_dict = permission_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    permission.sqlmodel_update(update_dict)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


def delete_permission(session: SessionDep, permission_id: int):
    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    session.delete(permission)
    session.commit()
    return Message(message="Permission deleted successfully")
