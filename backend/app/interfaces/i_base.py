from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")  # Entity / Model
ID = TypeVar("ID")  # Primary key type


class IBase(ABC, Generic[T, ID]):
    @abstractmethod
    def get(self, id: ID) -> T:
        ...

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 10) -> list[T]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def create(self, obj: T) -> T:
        ...

    @abstractmethod
    def update(self, obj: T, data: dict) -> T:
        ...

    @abstractmethod
    def delete(self, obj: T) -> None:
        ...
