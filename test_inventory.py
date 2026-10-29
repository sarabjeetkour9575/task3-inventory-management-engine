import csv
import json
import tempfile
import unittest
from pathlib import Path

from inventory_engine import (
    InventoryManager, Product, InvalidProductError, ProductNotFoundError,
    DuplicateProductError, InsufficientStockError, PersistenceError,
)

class ProductTests(unittest.TestCase):
    def test_product_validates_and_calculates_stock_value(self):
        p = Product(" P1 ", " Pen ", 4, 2.5)
        self.assertEqual(p.product_id, "P1")
        self.assertEqual(p.name, "Pen")
        self.assertEqual(p.stock_value, 10.0)
        self.assertEqual(Product.from_dict(p.to_dict()), p)

    def test_invalid_product_fields(self):
        for args in [
            ("", "Pen", 1, 2),
            ("P1", "", 1, 2),
            ("P1", "Pen", -1, 2),
            ("P1", "Pen", True, 2),
            ("P1", "Pen", 1, -2),
            ("P1", "Pen", 1, "bad"),
        ]:
            with self.subTest(args=args), self.assertRaises(InvalidProductError):
                Product(*args)

    def test_invalid_product_dictionary(self):
        with self.assertRaises(InvalidProductError):
            Product.from_dict({"product_id": "P1"})

class InventoryManagerTests(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryManager([Product("P2", "Book", 5, 10), Product("P1", "Pen", 10, 2)])

    def test_add_duplicate_and_wrong_type(self):
        with self.assertRaises(DuplicateProductError):
            self.inventory.add_product(Product("P1", "Another", 1, 1))
        with self.assertRaises(InvalidProductError):
            self.inventory.add_product("not a product")

    def test_get_missing_product(self):
        with self.assertRaises(ProductNotFoundError):
            self.inventory.get_product("missing")

    def test_list_sorted_and_total_value(self):
        self.assertEqual([p.product_id for p in self.inventory.list_products()], ["P1", "P2"])
        self.assertEqual(self.inventory.total_stock_value, 70.0)

    def test_update_product(self):
        p = self.inventory.update_product("P1", name="Marker", unit_price=3)
        self.assertEqual((p.name, p.unit_price), ("Marker", 3.0))
        with self.assertRaises(InvalidProductError):
            self.inventory.update_product("P1", name="")

    def test_restock_and_sell(self):
        self.assertEqual(self.inventory.restock("P1", 3).quantity, 13)
        self.assertEqual(self.inventory.sell("P1", 2).quantity, 11)
        with self.assertRaises(InsufficientStockError):
            self.inventory.sell("P1", 99)
        with self.assertRaises(InvalidProductError):
            self.inventory.restock("P1", 0)
        with self.assertRaises(InvalidProductError):
            self.inventory.sell("P1", -1)

    def test_unknown_id_for_operations(self):
        with self.assertRaises(ProductNotFoundError):
            self.inventory.sell("nope", 1)
        with self.assertRaises(ProductNotFoundError):
            self.inventory.restock("nope", 1)

class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.inventory = InventoryManager([Product("A1", "Notebook", 3, 25.5)])

    def test_json_round_trip(self):
        path = self.folder / "inventory.json"
        self.inventory.save(path)
        loaded = InventoryManager.load(path)
        self.assertEqual(loaded.get_product("A1").to_dict(), self.inventory.get_product("A1").to_dict())

    def test_csv_round_trip(self):
        path = self.folder / "inventory.csv"
        self.inventory.save(path)
        loaded = InventoryManager.load(path)
        self.assertEqual(loaded.get_product("A1").quantity, 3)

    def test_unsupported_extension(self):
        with self.assertRaises(PersistenceError):
            self.inventory.save(self.folder / "inventory.txt")
        with self.assertRaises(PersistenceError):
            InventoryManager.load(self.folder / "inventory.txt")

    def test_missing_and_malformed_files(self):
        with self.assertRaises(PersistenceError):
            InventoryManager.load(self.folder / "missing.json")
        bad = self.folder / "bad.json"
        bad.write_text("{not valid json", encoding="utf-8")
        with self.assertRaises(PersistenceError):
            InventoryManager.load(bad)

if __name__ == "__main__":
    unittest.main()
