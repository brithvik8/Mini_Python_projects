import sqlite3
from .config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            category TEXT,
            rarity TEXT,
            quantity INTEGER DEFAULT 0,
            threshold INTEGER DEFAULT 5,
            price REAL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            change_type TEXT,
            quantity_delta INTEGER,
            timestamp INTEGER,
            FOREIGN KEY(item_id) REFERENCES inventory_items(id)
        );
        """)
        conn.commit()
