from sqlmodel import Session

from app import crud
from app.models import ItemUnit, ItemUnitCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_item_unit(db: Session, user: User | None = None) -> ItemUnit:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    name = random_lower_string()
    description = random_lower_string()
    item_unit_in = ItemUnitCreate(name=name, description=description)
    return crud.create_item_unit(session=db, item_unit_in=item_unit_in, owner_id=owner_id)
