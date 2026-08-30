from .config import inventory_db
from .restock_request_gen import generate_restock_request

def check_item_alert(sku):
    if sku in inventory_db:
        item = inventory_db[sku]
        if item["quantity"] < item["threshold"]:
            print(f"[WARNING] CRITICAL ALERT: '{item['name']}' ({sku}) is low on stock! (Current: {item['quantity']}, Threshold: {item['threshold']})")
            generate_restock_request(item["name"], sku, item["threshold"] * 2)
