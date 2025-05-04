from sqlmodel import Session

from app import crud
from app.models import Store, StoreCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_latitude, random_longitude


def create_random_store(db: Session, user: User | None = None) -> Store:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    data = {
        "name": random_lower_string(),
        "address": random_lower_string(),
        "latitude": random_latitude(),
        "longitude": random_longitude(),
    }
    store_in = StoreCreate(**data)
    return crud.create_store(session=db, store_in=store_in, owner_id=owner_id)
