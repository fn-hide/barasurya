from sqlmodel import Session

from app import crud
from app.models import CustomerType, CustomerTypeCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_customer_type(db: Session, user: User | None = None) -> CustomerType:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    customer_type_in = CustomerTypeCreate(**data)
    return crud.create_customer_type(session=db, customer_type_in=customer_type_in, owner_id=owner_id)
