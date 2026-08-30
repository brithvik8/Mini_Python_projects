import os
import csv
import time

# 1. Local Database (In-Memory Dictionary)
inventory_db = {}

# 2. Database Initialization
def init_inventory():
    inventory_db.clear()

# 3. Add Item
def add_item(name, sku, category, rarity, quantity, threshold, price):
    if sku in inventory_db:
        print(f"Error: Item with SKU {sku} already exists.")
        return False
    
    inventory_db[sku] = {
        "name": name,
        "category": category,
        "rarity": rarity,
        "quantity": quantity,
        "threshold": threshold,
        "price": price
    }
    return True

# 4. Generate Restock Request
def generate_restock_request(name, sku, order_qty):
    os.makedirs("restock_requests", exist_ok=True)
    filepath = f"restock_requests/restock_{sku}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "Item Name", "Order Quantity", "Timestamp"])
        writer.writerow([sku, name, order_qty, int(time.time())])

# 5. Check Alerts
def check_item_alert(sku):
    if sku in inventory_db:
        item = inventory_db[sku]
        if item["quantity"] < item["threshold"]:
            print(f"[WARNING] CRITICAL ALERT: '{item['name']}' ({sku}) is low on stock! (Current: {item['quantity']}, Threshold: {item['threshold']})")
            generate_restock_request(item["name"], sku, item["threshold"] * 2)

# 6. Update Stock
def update_stock(sku, quantity_delta):
    if sku not in inventory_db:
        print(f"Error: SKU {sku} not found.")
        return False
        
    inventory_db[sku]["quantity"] += quantity_delta
    if inventory_db[sku]["quantity"] < 0:
        inventory_db[sku]["quantity"] = 0
        
    check_item_alert(sku)
    return True

# 7. Query Inventory
def query_inventory(search_query="", rarity=None, limit=50, offset=0):
    results = []
    search_query = search_query.lower()
    
    for sku, item in inventory_db.items():
        matches_query = search_query in item["name"].lower() or search_query in sku.lower()
        matches_rarity = (rarity is None) or (item["rarity"] == rarity)
        
        if matches_query and matches_rarity:
            results.append((sku, item["name"], item["category"], item["rarity"], item["quantity"], item["threshold"], item["price"]))
            
    paginated_results = results[offset : offset + limit]
    return paginated_results

# 8. Main Workflow
def main():
    init_inventory()
    
    print("Adding items...")
    add_item(
        name="Epic Sword of Fire",
        sku="SW-FIRE-001",
        category="Weapons",
        rarity="Epic",
        quantity=10,
        threshold=3,
        price=150.0
    )
    
    add_item(
        name="Health Potion",
        sku="POT-HEAL-002",
        category="Consumables",
        rarity="Common",
        quantity=2,
        threshold=5,
        price=10.0
    )
    
    print("\nChecking inventory stock alerts:")
    check_item_alert(sku="POT-HEAL-002")
    
    print("\nUpdating stock (using Health Potion)...")
    update_stock(sku="POT-HEAL-002", quantity_delta=5)
    
    print("\nQuerying weapons in inventory:")
    items = query_inventory(search_query="Sword", rarity="Epic")
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
