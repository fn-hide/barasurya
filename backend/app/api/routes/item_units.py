import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, and_

from app.api.deps import CurrentUser, SessionDep
from app.models import ItemUnit, ItemUnitCreate, ItemUnitPublic, ItemUnitsPublic, ItemUnitUpdate, Message, BaseModelUpdate

router = APIRouter(prefix="/item_units", tags=["item_units"])


@router.get("/", response_model=ItemUnitsPublic)
def read_item_units(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve item units.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(ItemUnit)
        count = session.exec(count_statement).one()
        statement = select(ItemUnit).offset(skip).limit(limit)
        item_units = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(ItemUnit)
            .where(ItemUnit.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(ItemUnit)
            .where(ItemUnit.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        item_units = session.exec(statement).all()

    return ItemUnitsPublic(data=item_units, count=count)


@router.get("/{id}", response_model=ItemUnitPublic)
def read_item_unit(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get item unit by ID.
    """
    item_unit = session.get(ItemUnit, id)
    if not item_unit:
        raise HTTPException(status_code=404, detail="Item unit not found")
    if not current_user.is_superuser and (item_unit.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item_unit


@router.post("/", response_model=ItemUnitPublic)
def create_item_unit(
    *, session: SessionDep, current_user: CurrentUser, item_unit_in: ItemUnitCreate
) -> Any:
    """
    Create new item unit.
    """
    item_unit = ItemUnit.model_validate(item_unit_in, update={"owner_id": current_user.id})
    session.add(item_unit)
    session.commit()
    session.refresh(item_unit)
    return item_unit


@router.put("/{id}", response_model=ItemUnitPublic)
def update_item_unit(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_unit_in: ItemUnitUpdate,
) -> Any:
    """
    Update an item unit.
    """
    item_unit = session.get(ItemUnit, id)
    if not item_unit:
        raise HTTPException(status_code=404, detail="Item unit not found")
    if not current_user.is_superuser and (item_unit.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_unit_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    item_unit.sqlmodel_update(update_dict)
    session.add(item_unit)
    session.commit()
    session.refresh(item_unit)
    return item_unit


@router.delete("/{id}")
def delete_item_unit(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an item unit.
    """
    item_unit = session.get(ItemUnit, id)
    if not item_unit:
        raise HTTPException(status_code=404, detail="Item unit not found")
    if not current_user.is_superuser and (item_unit.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item_unit)
    session.commit()
    return Message(message="Item deleted successfully")

# TODO: consider to add a feature for getting low stock item units
