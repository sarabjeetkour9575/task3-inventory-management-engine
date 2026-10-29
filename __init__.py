"""Object-oriented inventory management engine."""
from .manager import InventoryManager
from .models import Product
from .exceptions import (
    InventoryError, InvalidProductError, ProductNotFoundError,
    DuplicateProductError, InsufficientStockError, PersistenceError,
)

__all__ = [
    "InventoryManager", "Product", "InventoryError", "InvalidProductError",
    "ProductNotFoundError", "DuplicateProductError", "InsufficientStockError",
    "PersistenceError",
]
