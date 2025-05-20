from typing import Generic, TypeVar

from sqlmodel import func, select

from app.api.deps import SessionDep
from app.interfaces import IBase

T = TypeVar("T")  # Entity
ID = TypeVar("ID")  # Primary Key


class RBase(IBase[T, ID], Generic[T, ID]):
    def __init__(self, session: SessionDep, model: type[T]) -> None:
        self.session = session
        self.model = model

    def get(self, id: ID) -> T:
        return self.session.get(self.model, id)

    def list(self, skip=0, limit=0) -> list[T]:
        stmt = select(self.model).offset(skip).limit(limit)
        return self.session.exec(stmt).all()

    def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        return self.session.exec(stmt).one()

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T, data: dict) -> T:
        obj.sqlmodel_update(data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()
