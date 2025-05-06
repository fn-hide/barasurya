from sqlmodel import Session

from app import crud
from app.models import Customer, CustomerCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.customer_type import create_random_customer_type
from app.tests.utils.utils import random_lower_string


def create_random_customer(db: Session, user: User | None = None) -> Customer:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    
    customer_type = create_random_customer_type(db, user)
    customer_type_id = customer_type.id
    assert customer_type_id is not None
    
    data = {
        "name": random_lower_string(),
        "phone": random_lower_string(),
        "address": random_lower_string(),
        "customer_type_id": str(customer_type.id),
    }
    customer_in = CustomerCreate(**data)
    return crud.create_customer(session=db, customer_in=customer_in, owner_id=owner_id)
