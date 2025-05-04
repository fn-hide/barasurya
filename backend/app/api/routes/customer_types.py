import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import CustomerType, CustomerTypeCreate, CustomerTypePublic, CustomerTypesPublic, CustomerTypeUpdate, Message, BaseModelUpdate

router = APIRouter(prefix="/customer_types", tags=["customer_types"])


@router.get("/", response_model=CustomerTypesPublic)
def read_customer_types(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve customer types.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(CustomerType)
        count = session.exec(count_statement).one()
        statement = select(CustomerType).offset(skip).limit(limit)
        customer_types = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(CustomerType)
            .where(CustomerType.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(CustomerType)
            .where(CustomerType.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        customer_types = session.exec(statement).all()

    return CustomerTypesPublic(data=customer_types, count=count)


@router.get("/{id}", response_model=CustomerTypePublic)
def read_customer_type(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get customer type by ID.
    """
    customer_type = session.get(CustomerType, id)
    if not customer_type:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    if not current_user.is_superuser and (customer_type.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return customer_type


@router.post("/", response_model=CustomerTypePublic)
def create_customer_type(
    *, session: SessionDep, current_user: CurrentUser, customer_type_in: CustomerTypeCreate
) -> Any:
    """
    Create new customer type.
    """
    customer_type = CustomerType.model_validate(customer_type_in, update={"owner_id": current_user.id})
    session.add(customer_type)
    session.commit()
    session.refresh(customer_type)
    return customer_type


@router.put("/{id}", response_model=CustomerTypePublic)
def update_customer_type(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    customer_type_in: CustomerTypeUpdate,
) -> Any:
    """
    Update a customer_type.
    """
    customer_type = session.get(CustomerType, id)
    if not customer_type:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    if not current_user.is_superuser and (customer_type.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = customer_type_in.model_dump(exclude_unset=True)
    update_dict.update(BaseModelUpdate().model_dump())
    customer_type.sqlmodel_update(update_dict)
    session.add(customer_type)
    session.commit()
    session.refresh(customer_type)
    return customer_type


@router.delete("/{id}")
def delete_customer_type(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a customer type.
    """
    customer_type = session.get(CustomerType, id)
    if not customer_type:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    if not current_user.is_superuser and (customer_type.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(customer_type)
    session.commit()
    return Message(message="CustomerType deleted successfully")

# TODO: consider to add a feature for getting low stock customer_types
