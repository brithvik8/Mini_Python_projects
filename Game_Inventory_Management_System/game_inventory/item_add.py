from .config import inventory_db

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
