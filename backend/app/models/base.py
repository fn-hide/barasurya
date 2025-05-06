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
