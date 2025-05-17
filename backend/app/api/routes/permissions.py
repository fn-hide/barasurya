import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    BaseModelUpdate,
    Message,
    Permission,
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    PermissionUpdate,
)

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/", response_model=PermissionsPublic)
def read_permissions(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve permissions.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Permission)
        count = session.exec(count_statement).one()
        statement = select(Permission).offset(skip).limit(limit)
        permissions = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Permission)
            .where(Permission.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Permission)
            .where(Permission.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        permissions = session.exec(statement).all()

    return PermissionsPublic(data=permissions, count=count)


@router.get("/{id}", response_model=PermissionPublic)
def read_permission(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get permission by ID.
    """
    permission = session.get(Permission, id)
    if not permission:
        raise HTTPException(status_code=404, detail="permission not found")
    if not current_user.is_superuser and (permission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return permission


@router.post("/", response_model=PermissionPublic)
def create_permission(
    *, session: SessionDep, current_user: CurrentUser, permission_in: PermissionCreate
) -> Any:
    """
    Create new permission.
    """
    permission = Permission.model_validate(
        permission_in, update={"owner_id": current_user.id}
    )
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


@router.put("/{id}", response_model=PermissionPublic)
def update_permission(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    permission_in: PermissionUpdate,
) -> Any:
    """
    Update an permission.
    """
    permission = session.get(Permission, id)
    if not permission:
        raise HTTPException(status_code=404, detail="permission not found")
    if not current_user.is_superuser and (permission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = permission_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    permission.sqlmodel_update(update_dict)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission


@router.delete("/{id}")
def delete_permission(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an permission.
    """
    permission = session.get(Permission, id)
    if not permission:
        raise HTTPException(status_code=404, detail="permission not found")
    if not current_user.is_superuser and (permission.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(permission)
    session.commit()
    return Message(message="permission deleted successfully")
