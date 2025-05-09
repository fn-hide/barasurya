from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.base import BaseModel, BaseModelUpdate, SQLModel
else:
    from app.models.base import BaseModel, BaseModelUpdate, SQLModel  # type: ignore

from app.models.account import (
    Account,
    AccountCreate,
    AccountPublic,
    AccountsPublic,
    AccountUpdate,
)
from app.models.account_transaction import (
    AccountTransaction,
    AccountTransactionCreate,
    AccountTransactionPublic,
    AccountTransactionsPublic,
)
from app.models.customer import (
    Customer,
    CustomerCreate,
    CustomerPublic,
    CustomersPublic,
    CustomerUpdate,
)
from app.models.customer_type import (
    CustomerType,
    CustomerTypeCreate,
    CustomerTypePublic,
    CustomerTypesPublic,
    CustomerTypeUpdate,
)
from app.models.item import (
    Item,
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
)
from app.models.item_category import (
    ItemCategoriesPublic,
    ItemCategory,
    ItemCategoryCreate,
    ItemCategoryPublic,
    ItemCategoryUpdate,
)
from app.models.item_unit import (
    ItemUnit,
    ItemUnitCreate,
    ItemUnitPublic,
    ItemUnitsPublic,
    ItemUnitUpdate,
)
from app.models.main import (
    Message,
    NewPassword,
    Token,
    TokenPayload,
)
from app.models.payment import (
    Payment,
    PaymentCreate,
    PaymentPublic,
    PaymentsPublic,
)
from app.models.purchase import (
    Purchase,
    PurchaseCreate,
    PurchasePublic,
    PurchasesPublic,
    PurchaseUpdate,
)
from app.models.purchase_item import (
    PurchaseItem,
    PurchaseItemCreate,
    PurchaseItemPublic,
    PurchaseItemsPublic,
    PurchaseItemUpdate,
)
from app.models.sale import (
    Sale,
    SaleCreate,
    SalePublic,
    SalesPublic,
    SaleUpdate,
)
from app.models.sale_item import (
    SaleItem,
    SaleItemCreate,
    SaleItemPublic,
    SaleItemsPublic,
    SaleItemUpdate,
)
from app.models.store import (
    Store,
    StoreCreate,
    StorePublic,
    StoresPublic,
    StoreUpdate,
)
from app.models.supplier import (
    Supplier,
    SupplierCreate,
    SupplierPublic,
    SuppliersPublic,
    SupplierUpdate,
)
from app.models.user import (
    User,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserUpdate,
)

__all__ = [
    "SQLModel",
    "BaseModel",
    "BaseModelUpdate",
    "CustomerType",
    "CustomerTypeCreate",
    "CustomerTypeUpdate",
    "CustomerTypePublic",
    "CustomerTypesPublic",
    "Account",
    "AccountCreate",
    "AccountUpdate",
    "AccountPublic",
    "AccountsPublic",
    "AccountTransaction",
    "AccountTransactionCreate",
    "AccountTransactionPublic",
    "AccountTransactionsPublic",
    "Customer",
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerPublic",
    "CustomersPublic",
    "ItemCategory",
    "ItemCategoryCreate",
    "ItemCategoryUpdate",
    "ItemCategoryPublic",
    "ItemCategoriesPublic",
    "ItemUnit",
    "ItemUnitCreate",
    "ItemUnitUpdate",
    "ItemUnitPublic",
    "ItemUnitsPublic",
    "Item",
    "ItemCreate",
    "ItemUpdate",
    "ItemPublic",
    "ItemsPublic",
    "Message",
    "Token",
    "TokenPayload",
    "NewPassword",
    "Payment",
    "PaymentCreate",
    "PaymentPublic",
    "PaymentsPublic",
    "PurchaseItem",
    "PurchaseItemCreate",
    "PurchaseItemUpdate",
    "PurchaseItemPublic",
    "PurchaseItemsPublic",
    "Purchase",
    "PurchaseCreate",
    "PurchaseUpdate",
    "PurchasePublic",
    "PurchasesPublic",
    "SaleItem",
    "SaleItemCreate",
    "SaleItemUpdate",
    "SaleItemPublic",
    "SaleItemsPublic",
    "Sale",
    "SaleCreate",
    "SaleUpdate",
    "SalePublic",
    "SalesPublic",
    "Store",
    "StoreCreate",
    "StoreUpdate",
    "StorePublic",
    "StoresPublic",
    "Supplier",
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierPublic",
    "SuppliersPublic",
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UsersPublic",
]

# --- below same with above but auto-completion is not supported--- #
# import os
# import importlib
# import pkgutil


# # get the current directory name
# package_dir = os.path.dirname(__file__)
# package_name = __name__

# __all__ = []

# # auto-import all modules on this directory
# # loop every module (.py) inside this directory (except __init__.py)
# for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
#     if not is_pkg:
#         # Impor modulnya, misalnya models.item
#         module = importlib.import_module(f".{module_name}", package=package_name)

#         # Tambahkan semua objek yang tidak diawali _
#         for attr in dir(module):
#             if not attr.startswith("_"):
#                 globals()[attr] = getattr(module, attr)
#                 __all__.append(attr)

# TODO: consider to add "is_deleted" column (soft-delete)
