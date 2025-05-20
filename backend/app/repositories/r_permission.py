import uuid

from app.api.deps import SessionDep
from app.interfaces import IPermission
from app.models import Permission
from app.repositories import RBase


class RPermission(RBase[Permission, uuid.UUID], IPermission):
    def __init__(self, session: SessionDep) -> None:
        super().__init__(session, Permission)
