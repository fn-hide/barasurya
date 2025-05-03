from sqlmodel import Session

from app import crud
from app.models import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.item_category import create_random_item_category
from app.tests.utils.item_unit import create_random_item_unit
from app.tests.utils.utils import random_lower_string


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    
    item_category = create_random_item_category(db)
    item_category_id = item_category.id
    assert item_category_id is not None
    
    item_unit = create_random_item_unit(db)
    item_unit_id = item_unit.id
    assert item_unit_id is not None
    
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, item_category_id=item_category_id, item_unit_id=item_unit_id)
    return crud.create_item(session=db, item_in=item_in, owner_id=owner_id)
