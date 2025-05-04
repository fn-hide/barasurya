import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, BaseModelUpdate, ItemCategory, ItemCategoryCreate, ItemUnit, ItemUnitCreate, StoreCreate, Store


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    user_data.update(BaseModelUpdate().model_dump())
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item_category(*, session: Session, item_category_in: ItemCategoryCreate, owner_id: uuid.UUID) -> ItemCategory:
    db_item_category = ItemCategory.model_validate(item_category_in, update={"owner_id": owner_id})
    session.add(db_item_category)
    session.commit()
    session.refresh(db_item_category)
    return db_item_category


def create_item_unit(*, session: Session, item_unit_in: ItemUnitCreate, owner_id: uuid.UUID) -> ItemUnit:
    db_item_unit = ItemUnit.model_validate(item_unit_in, update={"owner_id": owner_id})
    session.add(db_item_unit)
    session.commit()
    session.refresh(db_item_unit)
    return db_item_unit


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_store(*, session: Session, store_in: StoreCreate, owner_id: uuid.UUID) -> Store:
    db_store = Store.model_validate(store_in, update={"owner_id": owner_id})
    session.add(db_store)
    session.commit()
    session.refresh(db_store)
    return db_store
