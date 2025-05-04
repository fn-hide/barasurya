import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Supplier, SupplierCreate, SupplierPublic, SuppliersPublic, SupplierUpdate, Message, BaseModelUpdate

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("/", response_model=SuppliersPublic)
def read_suppliers(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve suppliers.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Supplier)
        count = session.exec(count_statement).one()
        statement = select(Supplier).offset(skip).limit(limit)
        suppliers = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Supplier)
            .where(Supplier.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Supplier)
            .where(Supplier.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        suppliers = session.exec(statement).all()

    return SuppliersPublic(data=suppliers, count=count)


@router.get("/{id}", response_model=SupplierPublic)
def read_supplier(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get supplier by ID.
    """
    supplier = session.get(Supplier, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    if not current_user.is_superuser and (supplier.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return supplier


@router.post("/", response_model=SupplierPublic)
def create_supplier(
    *, session: SessionDep, current_user: CurrentUser, supplier_in: SupplierCreate
) -> Any:
    """
    Create new supplier.
    """
    supplier = Supplier.model_validate(supplier_in, update={"owner_id": current_user.id})
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    return supplier


@router.put("/{id}", response_model=SupplierPublic)
def update_supplier(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    supplier_in: SupplierUpdate,
) -> Any:
    """
    Update a supplier.
    """
    supplier = session.get(Supplier, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    if not current_user.is_superuser and (supplier.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = supplier_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    supplier.sqlmodel_update(update_dict)
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    return supplier


@router.delete("/{id}")
def delete_supplier(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a supplier.
    """
    supplier = session.get(Supplier, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    if not current_user.is_superuser and (supplier.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(supplier)
    session.commit()
    return Message(message="Supplier deleted successfully")

# TODO: consider to add a feature for getting low stock suppliers
