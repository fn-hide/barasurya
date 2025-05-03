from sqlmodel import Session

from app import crud
from app.models import ItemCategory, ItemCategoryCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_item_category(db: Session, user: User | None = None) -> ItemCategory:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    
    name = random_lower_string()
    description = random_lower_string()
    item_category_in = ItemCategoryCreate(name=name, description=description)
    return crud.create_item_category(session=db, item_category_in=item_category_in, owner_id=owner_id)
