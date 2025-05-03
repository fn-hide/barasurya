import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, and_

from app.api.deps import CurrentUser, SessionDep
from app.models import ItemCategory, ItemCategoryCreate, ItemCategoryPublic, ItemCategoriesPublic, ItemCategoryUpdate, Message, BaseModelUpdate

router = APIRouter(prefix="/item_categories", tags=["item_categories"])


@router.get("/", response_model=ItemCategoriesPublic)
def read_item_categories(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve item categories.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(ItemCategory)
        count = session.exec(count_statement).one()
        statement = select(ItemCategory).offset(skip).limit(limit)
        item_categories = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(ItemCategory)
            .where(ItemCategory.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(ItemCategory)
            .where(ItemCategory.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        item_categories = session.exec(statement).all()

    return ItemCategoriesPublic(data=item_categories, count=count)


@router.get("/{id}", response_model=ItemCategoryPublic)
def read_item_category(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get item category by ID.
    """
    item_category = session.get(ItemCategory, id)
    if not item_category:
        raise HTTPException(status_code=404, detail="Item category not found")
    if not current_user.is_superuser and (item_category.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item_category


@router.post("/", response_model=ItemCategoryPublic)
def create_item_category(
    *, session: SessionDep, current_user: CurrentUser, item_category_in: ItemCategoryCreate
) -> Any:
    """
    Create new item category.
    """
    item_category = ItemCategory.model_validate(item_category_in, update={"owner_id": current_user.id})
    session.add(item_category)
    session.commit()
    session.refresh(item_category)
    return item_category


@router.put("/{id}", response_model=ItemCategoryPublic)
def update_item_category(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_category_in: ItemCategoryUpdate,
) -> Any:
    """
    Update an item category.
    """
    item_category = session.get(ItemCategory, id)
    if not item_category:
        raise HTTPException(status_code=404, detail="Item category not found")
    if not current_user.is_superuser and (item_category.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_category_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    item_category.sqlmodel_update(update_dict)
    session.add(item_category)
    session.commit()
    session.refresh(item_category)
    return item_category


@router.delete("/{id}")
def delete_item_category(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an item category.
    """
    item_category = session.get(ItemCategory, id)
    if not item_category:
        raise HTTPException(status_code=404, detail="Item category not found")
    if not current_user.is_superuser and (item_category.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item_category)
    session.commit()
    return Message(message="Item category deleted successfully")

# TODO: consider to add a feature for getting low stock item categories
