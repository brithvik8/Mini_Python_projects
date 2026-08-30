import sqlite3
from .config import DB_PATH
from .restock_request_gen import generate_restock_request

def check_item_alert(item_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, threshold, sku FROM inventory_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if row and row[1] < row[2]:
            print(f"⚠️ CRITICAL ALERT: '{row[0]}' ({row[3]}) is low on stock! (Current: {row[1]}, Threshold: {row[2]})")
            generate_restock_request(row[0], row[3], row[2] * 2)
