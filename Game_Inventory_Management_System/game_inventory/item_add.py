import sqlite3
import time
from .config import DB_PATH

def add_item(name, sku, category, rarity, quantity, threshold, price):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO inventory_items (name, sku, category, rarity, quantity, threshold, price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, sku, category, rarity, quantity, threshold, price))
            item_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO audit_logs (item_id, change_type, quantity_delta, timestamp)
                VALUES (?, 'INITIAL_ADD', ?, ?)
            """, (item_id, quantity, int(time.time())))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"SKU violation or integrity error: {e}")
            conn.rollback()
            return False
