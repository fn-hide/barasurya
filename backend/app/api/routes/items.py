import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, and_

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate, BaseModelUpdate, Message, ItemCategory

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Item)
        count = session.exec(count_statement).one()
        statement = select(Item).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Item)
            .where(Item.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .where(Item.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return ItemsPublic(data=items, count=count)


@router.get("/{id}", response_model=ItemPublic)
def read_item(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    item_category = session.get(ItemCategory, item_in.item_category_id)
    if not item_category:
        raise HTTPException(status_code=404, detail="Item category not found")
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{id}")
def delete_item(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")


@router.put("/{id}/stock", response_model=ItemPublic)
def update_stock_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    quantity: int,
) -> Any:
    """
    Update an item stock.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item.stock += quantity
    item.sqlmodel_update(BaseModelUpdate().model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/low_stock/", response_model=ItemsPublic)
def read_low_stock_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve low stock items.
    """

    if current_user.is_superuser:
        count_statement = (
            select(func.count())
            .select_from(Item)
            .where(Item.stock <= Item.stock_minimum)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .where(Item.stock <= Item.stock_minimum)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Item)
            .where(and_(
                Item.owner_id == current_user.id,
                Item.stock <= Item.stock_minimum,
            ))
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Item)
            .where(and_(
                Item.owner_id == current_user.id,
                Item.stock <= Item.stock_minimum,
            ))
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return ItemsPublic(data=items, count=count)


@router.put("/{id}/activate", response_model=ItemPublic)
def activate_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    """
    Update an item stock.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item.is_active = True
    item.sqlmodel_update(BaseModelUpdate().model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}/deactivate", response_model=ItemPublic)
def deactivate_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    """
    Update an item stock.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item.is_active = False
    item.sqlmodel_update(BaseModelUpdate().model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
