import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import (
    Message,
    Permission,
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    PermissionUpdate,
)
from app.repositories import RPermission
from app.services import SPermission
from app.utils import utcnow

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionPublic,
)
def read_permission(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get permission by ID.
    """
    repo = RPermission(session)
    service = SPermission(repo)
    try:
        return service.read_permission(id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionsPublic,
)
def read_permissions(session: SessionDep, skip: int = 0, limit: int = 10) -> Any:
    """
    Retrieve permissions.
    """
    repo = RPermission(session)
    service = SPermission(repo)
    return service.read_permissions(skip, limit)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionPublic,
)
def create_permission(
    *, session: SessionDep, current_user: CurrentUser, permission_in: PermissionCreate
) -> Any:
    """
    Create new permission.
    """
    permission = Permission.model_validate(
        permission_in, update={"owner_id": current_user.id}
    )
    repo = RPermission(session)
    service = SPermission(repo)
    return service.create_permission(permission)


@router.put(
    "/{id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionPublic,
)
def update_permission(
    *,
    session: SessionDep,
    id: uuid.UUID,
    permission_in: PermissionUpdate,
) -> Any:
    """
    Update an permission.
    """
    repo = RPermission(session)
    service = SPermission(repo)
    try:
        permission = service.read_permission(id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    update_dict = permission_in.model_dump(exclude_unset=True)
    update_dict.date_updated = str(utcnow())
    permission.sqlmodel_update(update_dict)
    return service.update_permission(permission, update_dict)


@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_permission(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete an permission.
    """
    repo = RPermission(session)
    service = SPermission(repo)
    try:
        permission = service.read_permission(id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    return service.delete_permission(permission)
