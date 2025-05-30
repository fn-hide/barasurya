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
    Token,
    TokenPayload,
)
from app.models.payable import (
    Payable,
    PayableCreate,
    PayablePublic,
    PayablesPublic,
    PayableUpdate,
)
from app.models.payment import (
    Payment,
    PaymentCreate,
    PaymentPublic,
    PaymentsPublic,
)
from app.models.permission import (
    Permission,
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    PermissionUpdate,
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
from app.models.purchase_return import (
    PurchaseReturn,
    PurchaseReturnCreate,
    PurchaseReturnPublic,
    PurchaseReturnsPublic,
    PurchaseReturnUpdate,
)
from app.models.purchase_return_item import (
    PurchaseReturnItem,
    PurchaseReturnItemCreate,
    PurchaseReturnItemPublic,
    PurchaseReturnItemsPublic,
    PurchaseReturnItemUpdate,
)
from app.models.receivable import (
    Receivable,
    ReceivableCreate,
    ReceivablePublic,
    ReceivablesPublic,
    ReceivableUpdate,
)
from app.models.role import (
    Role,
    RoleCreate,
    RolePublic,
    RolesPublic,
    RoleUpdate,
)
from app.models.role_permission import (
    RolePermission,
    RolePermissionCreate,
    RolePermissionPublic,
    RolePermissionsPublic,
    RolePermissionUpdate,
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
from app.models.sale_return import (
    SaleReturn,
    SaleReturnCreate,
    SaleReturnPublic,
    SaleReturnsPublic,
    SaleReturnUpdate,
)
from app.models.sale_return_item import (
    SaleReturnItem,
    SaleReturnItemCreate,
    SaleReturnItemPublic,
    SaleReturnItemsPublic,
    SaleReturnItemUpdate,
)
from app.models.stock_adjustment import (
    StockAdjustment,
    StockAdjustmentCreate,
    StockAdjustmentPublic,
    StockAdjustmentsPublic,
)
from app.models.stock_transfer import (
    StockTransfer,
    StockTransferCreate,
    StockTransferPublic,
    StockTransfersPublic,
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
    NewPassword,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.models.user_role import (
    UserRole,
    UserRoleCreate,
    UserRolePublic,
    UserRolesPublic,
    UserRoleUpdate,
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
    "PurchaseReturn",
    "PurchaseReturnCreate",
    "PurchaseReturnUpdate",
    "PurchaseReturnPublic",
    "PurchaseReturnsPublic",
    "Role",
    "RoleCreate",
    "RoleUpdate",
    "RolePublic",
    "RolesPublic",
    "Permission",
    "PermissionCreate",
    "PermissionUpdate",
    "PermissionPublic",
    "PermissionsPublic",
    "UserRole",
    "UserRoleCreate",
    "UserRoleUpdate",
    "UserRolePublic",
    "UserRolesPublic",
    "RolePermission",
    "RolePermissionCreate",
    "RolePermissionUpdate",
    "RolePermissionPublic",
    "RolePermissionsPublic",
    "SaleReturn",
    "SaleReturnCreate",
    "SaleReturnUpdate",
    "SaleReturnPublic",
    "SaleReturnsPublic",
    "PurchaseReturnItem",
    "PurchaseReturnItemCreate",
    "PurchaseReturnItemUpdate",
    "PurchaseReturnItemPublic",
    "PurchaseReturnItemsPublic",
    "SaleReturnItem",
    "SaleReturnItemCreate",
    "SaleReturnItemUpdate",
    "SaleReturnItemPublic",
    "SaleReturnItemsPublic",
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
    "StockAdjustment",
    "StockAdjustmentCreate",
    "StockAdjustmentPublic",
    "StockAdjustmentsPublic",
    "StockTransfer",
    "StockTransferCreate",
    "StockTransferPublic",
    "StockTransfersPublic",
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
    "UpdatePassword",
    "UserRegister",
    "UserUpdateMe",
    "Payable",
    "PayableCreate",
    "PayableUpdate",
    "PayablePublic",
    "PayablesPublic",
    "Receivable",
    "ReceivableCreate",
    "ReceivableUpdate",
    "ReceivablePublic",
    "ReceivablesPublic",
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
