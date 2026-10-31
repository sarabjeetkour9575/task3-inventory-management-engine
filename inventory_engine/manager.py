"""Business logic for the inventory engine."""
from .exceptions import (
    DuplicateProductError, ProductNotFoundError, InsufficientStockError,
    InvalidProductError,
)
from .models import Product
from .storage import load_products, save_products

class InventoryManager:
    """Manage products and keep inventory rules in one place."""

    def __init__(self, products=None):
        self._products = {}
        for product in products or []:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise InvalidProductError("Expected a Product object.")
        if product.product_id in self._products:
            raise DuplicateProductError(f"Product ID '{product.product_id}' already exists.")
        self._products[product.product_id] = product

    def get_product(self, product_id: str) -> Product:
        key = str(product_id).strip()
        try:
            return self._products[key]
        except KeyError as exc:
            raise ProductNotFoundError(f"Product ID '{key}' was not found.") from exc

    def list_products(self):
        return sorted(self._products.values(), key=lambda product: product.product_id)

    def update_product(self, product_id: str, *, name=None, unit_price=None) -> Product:
        product = self.get_product(product_id)
        new_name = product.name if name is None else str(name).strip()
        new_price = product.unit_price if unit_price is None else unit_price
        # Validate before mutating the existing object.
        validated = Product(product.product_id, new_name, product.quantity, new_price)
        self._products[product.product_id] = validated
        return validated

    def restock(self, product_id: str, quantity: int) -> Product:
        product = self.get_product(product_id)
        self._validate_quantity(quantity)
        updated = Product(product.product_id, product.name, product.quantity + quantity, product.unit_price)
        self._products[product.product_id] = updated
        return updated

    def sell(self, product_id: str, quantity: int) -> Product:
        product = self.get_product(product_id)
        self._validate_quantity(quantity)
        if quantity > product.quantity:
            raise InsufficientStockError(
                f"Cannot sell {quantity}; only {product.quantity} item(s) are in stock."
            )
        updated = Product(product.product_id, product.name, product.quantity - quantity, product.unit_price)
        self._products[product.product_id] = updated
        return updated

    @staticmethod
    def _validate_quantity(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise InvalidProductError("Quantity must be a positive whole number.")

    @property
    def total_stock_value(self) -> float:
        return round(sum(p.stock_value for p in self._products.values()), 2)

    def save(self, file_path) -> None:
        save_products(self.list_products(), file_path)

    @classmethod
    def load(cls, file_path) -> "InventoryManager":
        return cls(load_products(file_path))
