import uuid

from sqlmodel import Session

from app.models import (
    Customer,
    CustomerCreate,
)


def create_customer(
    *, session: Session, customer_in: CustomerCreate, owner_id: uuid.UUID
) -> Customer:
    db_customer = Customer.model_validate(customer_in, update={"owner_id": owner_id})
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer
