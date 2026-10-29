# Object-Oriented Inventory Management Engine

A modular Python project for **Core Algorithms, OOP Structures & Robust Error Handling**. It models a small inventory system with custom exceptions, validated data, JSON/CSV persistence, a command-line demo, and automated unit tests.

## Features
- `Product` data model with validation and stock valuation.
- `InventoryManager` for add, list, update, restock, sell, and total stock value.
- Custom exceptions for invalid data, duplicate IDs, missing products, insufficient stock, and persistence errors.
- Save/load inventory using JSON or CSV.
- Automated `unittest` test suite.

## Project structure
```text
task3-inventory-engine/
├── inventory_engine/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── models.py
│   ├── manager.py
│   ├── storage.py
│   └── cli.py
├── tests/
│   └── test_inventory.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements
Python 3.10 or newer. The project uses only the Python standard library.

## Run the demo
From the project root:
```bash
python -m inventory_engine.cli
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Test coverage
Install the optional coverage package and run:
```bash
python -m pip install coverage
coverage run -m unittest discover -s tests
coverage report -m
```
The tests cover valid and invalid product data, inventory operations, custom error paths, and JSON/CSV persistence. Coverage percentage can vary by coverage tool/version; check the report before claiming a specific result.

## Example
```python
from inventory_engine import InventoryManager, Product

store = InventoryManager()
store.add_product(Product("P101", "Notebook", 20, 35.0))
store.sell("P101", 2)
store.save("inventory.json")
print(store.total_stock_value)
```
