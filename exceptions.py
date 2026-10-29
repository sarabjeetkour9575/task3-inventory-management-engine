"""Custom exceptions used by the inventory engine."""

class InventoryError(Exception):
    """Base class for expected inventory errors."""

class InvalidProductError(InventoryError):
    """Raised when product details are invalid."""

class ProductNotFoundError(InventoryError):
    """Raised when a requested product does not exist."""

class DuplicateProductError(InventoryError):
    """Raised when a product ID already exists."""

class InsufficientStockError(InventoryError):
    """Raised when a stock operation would make stock negative."""

class PersistenceError(InventoryError):
    """Raised when data cannot be saved or loaded."""
