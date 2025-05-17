import uuid

from sqlmodel import Session

from app.models import (
    Supplier,
    SupplierCreate,
)


def create_supplier(
    *, session: Session, supplier_in: SupplierCreate, owner_id: uuid.UUID
) -> Supplier:
    db_supplier = Supplier.model_validate(supplier_in, update={"owner_id": owner_id})
    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier
