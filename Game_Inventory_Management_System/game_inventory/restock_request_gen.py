import os
import csv
import time

def generate_restock_request(name, sku, order_qty):
    os.makedirs("restock_requests", exist_ok=True)
    filepath = f"restock_requests/restock_{sku}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "Item Name", "Order Quantity", "Timestamp"])
        writer.writerow([sku, name, order_qty, int(time.time())])
