# 1. Local Database (In-Memory Dictionary)
inventory_db = {}

# 2. Initialization of Database
def init_inventory():
    inventory_db.clear()

# 3. Adding Item
def add_item(name, item_code, category, rarity, quantity, threshold, price):
    if item_code in inventory_db:
        print(f"Error: Item with code {item_code} already exists.")
        return False
    
    inventory_db[item_code] = {
        "name": name,
        "category": category,
        "rarity": rarity,
        "quantity": quantity,
        "threshold": threshold,
        "price": price
    }
    return True

# 4. Generating Restock Request
def generate_restock_request(name, item_code, order_qty):
    filepath = f"restock_{item_code}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Item Code: {item_code}\n")
        f.write(f"Item Name: {name}\n")
        f.write(f"Order Quantity: {order_qty}\n")

# 5. Checking Alerts
def check_item_alert(item_code):
    if item_code in inventory_db:
        item = inventory_db[item_code]
        if item["quantity"] < item["threshold"]:
            print(f"[WARNING] CRITICAL ALERT: '{item['name']}' ({item_code}) is low on stock! (Current: {item['quantity']}, Threshold: {item['threshold']})")
            generate_restock_request(item["name"], item_code, item["threshold"] * 2)

# 6. Updating Stock
def update_stock(item_code, quantity_delta):
    if item_code not in inventory_db:
        print(f"Error: Item code {item_code} not found.")
        return False
        
    inventory_db[item_code]["quantity"] += quantity_delta
    if inventory_db[item_code]["quantity"] < 0:
        inventory_db[item_code]["quantity"] = 0
        
    check_item_alert(item_code)
    return True

# 7. Query Inventory
def query_inventory(search_query="", rarity=None, limit=50, offset=0):
    results = []
    search_query = search_query.lower()
    
    for item_code, item in inventory_db.items():
        matches_query = search_query in item["name"].lower() or search_query in item_code.lower()
        matches_rarity = (rarity is None) or (item["rarity"] == rarity)
        
        if matches_query and matches_rarity:
            results.append((item_code, item["name"], item["category"], item["rarity"], item["quantity"], item["threshold"], item["price"]))
            
    paginated_results = results[offset : offset + limit]
    return paginated_results

# 8. Main Workflow
def main():
    init_inventory()
    
    print("Adding items...")
    add_item(
        name="Epic Sword of Fire",
        item_code="SWD1",
        category="Weapons",
        rarity="Epic",
        quantity=10,
        threshold=3,
        price=150.0
    )
    
    add_item(
        name="Health Potion",
        item_code="POT2",
        category="Consumables",
        rarity="Common",
        quantity=2,
        threshold=5,
        price=10.0
    )
    
    print("\nChecking inventory stock alerts:")
    check_item_alert(item_code="POT2")
    
    print("\nUpdating stock (using Health Potion)...")
    update_stock(item_code="POT2", quantity_delta=5)
    
    print("\nQuerying weapons in inventory:")
    items = query_inventory(search_query="Sword", rarity="Epic")
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
