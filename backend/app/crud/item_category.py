import uuid

from sqlmodel import Session

from app.models import (
    ItemCategory,
    ItemCategoryCreate,
)


def create_item_category(
    *, session: Session, item_category_in: ItemCategoryCreate, owner_id: uuid.UUID
) -> ItemCategory:
    db_item_category = ItemCategory.model_validate(
        item_category_in, update={"owner_id": owner_id}
    )
    session.add(db_item_category)
    session.commit()
    session.refresh(db_item_category)
    return db_item_category
