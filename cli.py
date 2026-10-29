"""Small command-line demonstration."""
from . import InventoryManager, Product, InventoryError

def main():
    inventory = InventoryManager()
    print("Inventory Engine demo (type 'q' to quit)")
    while True:
        print("\n1 Add product  2 List products  3 Restock  4 Sell  5 Save JSON  q Quit")
        choice = input("Choose: ").strip().lower()
        try:
            if choice == "q":
                break
            if choice == "1":
                inventory.add_product(Product(
                    input("ID: "), input("Name: "),
                    int(input("Quantity: ")), float(input("Unit price: "))
                ))
                print("Product added.")
            elif choice == "2":
                for product in inventory.list_products():
                    print(f"{product.product_id}: {product.name} | qty={product.quantity} | price={product.unit_price:.2f}")
                print(f"Total stock value: {inventory.total_stock_value:.2f}")
            elif choice == "3":
                inventory.restock(input("Product ID: "), int(input("Quantity to add: ")))
                print("Stock updated.")
            elif choice == "4":
                inventory.sell(input("Product ID: "), int(input("Quantity to sell: ")))
                print("Sale recorded.")
            elif choice == "5":
                inventory.save(input("File path (e.g. inventory.json): ").strip())
                print("Inventory saved.")
            else:
                print("Choose one of the listed options.")
        except (ValueError, InventoryError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
