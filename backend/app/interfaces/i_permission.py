import uuid

from app.models import Permission

from .i_base import IBase


class IPermission(IBase[Permission, uuid.UUID]):
    pass
