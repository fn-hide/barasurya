from fastapi import APIRouter

from app.api.routes import (
    customer_types,
    customers,
    item_categories,
    item_units,
    items,
    login,
    permissions,
    private,
    stores,
    suppliers,
    users,
    utils,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(customer_types.router)
api_router.include_router(customers.router)
api_router.include_router(item_categories.router)
api_router.include_router(item_units.router)
api_router.include_router(items.router)
api_router.include_router(login.router)
api_router.include_router(permissions.router)
api_router.include_router(stores.router)
api_router.include_router(suppliers.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
