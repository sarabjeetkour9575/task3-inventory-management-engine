"""Domain models for inventory management."""
from dataclasses import dataclass
from .exceptions import InvalidProductError

@dataclass
class Product:
    """A product held in inventory."""
    product_id: str
    name: str
    quantity: int
    unit_price: float

    def __post_init__(self):
        self.product_id = str(self.product_id).strip()
        self.name = str(self.name).strip()
        if not self.product_id:
            raise InvalidProductError("Product ID cannot be empty.")
        if not self.name:
            raise InvalidProductError("Product name cannot be empty.")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int):
            raise InvalidProductError("Quantity must be a whole number.")
        if self.quantity < 0:
            raise InvalidProductError("Quantity cannot be negative.")
        if isinstance(self.unit_price, bool) or not isinstance(self.unit_price, (int, float)):
            raise InvalidProductError("Unit price must be numeric.")
        if self.unit_price < 0:
            raise InvalidProductError("Unit price cannot be negative.")
        self.unit_price = float(self.unit_price)

    @property
    def stock_value(self) -> float:
        """Return the total value of this product's current stock."""
        return round(self.quantity * self.unit_price, 2)

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        try:
            return cls(
                product_id=data["product_id"],
                name=data["name"],
                quantity=int(data["quantity"]),
                unit_price=float(data["unit_price"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidProductError(f"Invalid product data: {exc}") from exc
