import uuid

from app.models import (
    Permission,
    PermissionPublic,
    PermissionsPublic,
)
from app.repositories import RPermission


class SPermission:
    def __init__(self, repo: RPermission) -> None:
        self.repo = repo

    def read_permission(self, id: uuid.UUID) -> PermissionPublic:
        obj = self.repo.get(id)
        if not obj:
            raise ValueError("Permission not found")
        return obj

    def read_permissions(self, skip=0, limit=10) -> PermissionsPublic:
        objs = self.repo.list()
        count = self.repo.count()
        return PermissionsPublic(data=objs, count=count)

    def create_permission(self, obj: Permission):
        return self.repo.create(obj)

    def update_permission(self, obj: Permission, data: dict):
        return self.repo.update(obj, data)

    def delete_permission(self, id: uuid.UUID):
        return self.repo.delete(id)
