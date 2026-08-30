import sqlite3
from .config import DB_PATH

def query_inventory(search_query="", rarity=None, limit=50, offset=0):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM inventory_items WHERE (name LIKE ? OR sku LIKE ?)"
        params = [f"%{search_query}%", f"%{search_query}%"]
        
        if rarity:
            sql += " AND rarity = ?"
            params.append(rarity)
            
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(sql, params)
        return cursor.fetchall()
