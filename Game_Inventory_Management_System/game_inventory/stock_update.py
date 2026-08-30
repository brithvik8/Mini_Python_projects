import sqlite3
import time
from .config import DB_PATH
from .alert_check import check_item_alert

def update_stock(item_id, quantity_delta):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE inventory_items 
                SET quantity = quantity + ? 
                WHERE id = ?
            """, (quantity_delta, item_id))
            
            cursor.execute("""
                INSERT INTO audit_logs (item_id, change_type, quantity_delta, timestamp)
                VALUES (?, 'STOCK_ADJUST', ?, ?)
            """, (item_id, quantity_delta, int(time.time())))
            conn.commit()
            
            check_item_alert(item_id)
            return True
        except Exception as e:
            print(f"Transaction failed: {e}")
            conn.rollback()
            return False
