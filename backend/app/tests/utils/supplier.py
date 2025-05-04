from sqlmodel import Session

from app import crud
from app.models import Supplier, SupplierCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_supplier(db: Session, user: User | None = None) -> Supplier:
    if user is None:
        user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    data = {
        "name": random_lower_string(),
        "phone": random_lower_string(),
        "address": random_lower_string(),
    }
    supplier_in = SupplierCreate(**data)
    return crud.create_supplier(session=db, supplier_in=supplier_in, owner_id=owner_id)
