"""JSON and CSV persistence helpers."""
import csv
import json
from pathlib import Path
from .exceptions import PersistenceError
from .models import Product

CSV_FIELDS = ["product_id", "name", "quantity", "unit_price"]

def save_products(products, file_path):
    """Save products to JSON or CSV based on file extension."""
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        records = [p.to_dict() for p in products]
        suffix = path.suffix.lower()
        if suffix == ".json":
            path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        elif suffix == ".csv":
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
                writer.writeheader()
                writer.writerows(records)
        else:
            raise PersistenceError("Unsupported file type. Use .json or .csv.")
    except PersistenceError:
        raise
    except (OSError, TypeError, ValueError) as exc:
        raise PersistenceError(f"Could not save inventory: {exc}") from exc

def load_products(file_path):
    """Load products from JSON or CSV and return Product objects."""
    path = Path(file_path)
    try:
        suffix = path.suffix.lower()
        if suffix == ".json":
            records = json.loads(path.read_text(encoding="utf-8"))
        elif suffix == ".csv":
            with path.open("r", newline="", encoding="utf-8") as handle:
                records = list(csv.DictReader(handle))
        else:
            raise PersistenceError("Unsupported file type. Use .json or .csv.")
        if not isinstance(records, list):
            raise PersistenceError("Inventory file must contain a list of products.")
        return [Product.from_dict(row) for row in records]
    except PersistenceError:
        raise
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise PersistenceError(f"Could not load inventory: {exc}") from exc
