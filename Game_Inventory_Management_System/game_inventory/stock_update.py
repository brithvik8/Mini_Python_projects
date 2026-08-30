from .config import inventory_db
from .alert_check import check_item_alert

def update_stock(sku, quantity_delta):
    if sku not in inventory_db:
        print(f"Error: SKU {sku} not found.")
        return False
        
    inventory_db[sku]["quantity"] += quantity_delta
    # Prevent negative stock count
    if inventory_db[sku]["quantity"] < 0:
        inventory_db[sku]["quantity"] = 0
        
    check_item_alert(sku)
    return True
