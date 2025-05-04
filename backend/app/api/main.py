from fastapi import APIRouter

from app.api.routes import items, item_categories, item_units, stores, suppliers, customer_types, customers, login, private, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(item_categories.router)
api_router.include_router(item_units.router)
api_router.include_router(stores.router)
api_router.include_router(suppliers.router)
api_router.include_router(customer_types.router)
api_router.include_router(customers.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
