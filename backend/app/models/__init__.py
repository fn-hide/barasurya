# import os
# import importlib
# import pkgutil
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from app.utils import utcnow


# setup constraint naming convention, so we add flexibility to modify constraint later
# source: https://github.com/fastapi/sqlmodel/discussions/1213
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseModel(SQLModel):
    """Base model for everything by add naming convention feature."""

    model_config = ConfigDict(
        protected_namespaces=(),
    )  # type: ignore


BaseModel.metadata.naming_convention = convention


class BaseModelUpdate(BaseModel):
    date_updated: datetime = Field(default_factory=utcnow)


from app.models.main import *
from app.models.user import *
from app.models.item_category import *
from app.models.item_unit import *
from app.models.item import *

# --- below same with above but auto-completion is not supported--- #
# # get the current directory name
# package_dir = os.path.dirname(__file__)
# package_name = __name__

# __all__ = []

# # auto-import all modules on this directory
# # loop every module (.py) inside this directory (except __init__.py)
# for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
#     if not is_pkg:
#         # Impor modulnya, misalnya models.item
#         module = importlib.import_module(f".{module_name}", package=package_name)

#         # Tambahkan semua objek yang tidak diawali _
#         for attr in dir(module):
#             if not attr.startswith("_"):
#                 globals()[attr] = getattr(module, attr)
#                 __all__.append(attr)

# TODO: consider to add "is_deleted" column (soft-delete)
