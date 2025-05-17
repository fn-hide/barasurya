import uuid

from sqlmodel import Session

from app.models import (
    ItemUnit,
    ItemUnitCreate,
)


def create_item_unit(
    *, session: Session, item_unit_in: ItemUnitCreate, owner_id: uuid.UUID
) -> ItemUnit:
    db_item_unit = ItemUnit.model_validate(item_unit_in, update={"owner_id": owner_id})
    session.add(db_item_unit)
    session.commit()
    session.refresh(db_item_unit)
    return db_item_unit
