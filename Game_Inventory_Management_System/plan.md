# Project Plan: Game Inventory Management System

## 1. Project Overview
A robust, modern desktop inventory manager designed for game items, gear, assets, and catalog resources. Tracks stock volumes, item parameters, rarity levels, storage configurations, and historical inventory audits.

## 2. General Requirements
- Language: Python 3.12+
- Platform: Cross-platform (Windows/macOS/Linux)
- Database: Local SQLite with transaction integrity checks.
- Export format: CSV, JSON reporting.
## 3. Development Milestones
- **Milestone 1: Database Model & ACID Transactions**
  - Design SQL schema for item inventories, locations, and audit logs.
- **Milestone 2: CRUD & Search Filters**
  - Write search index query parameters to filter items by rarity, stock level, or category.
- **Milestone 3: Low Stock Alerts & Order Trigger Engine**
  - Implement automated notification thresholds when item counts drop below safety margins.
- **Milestone 4: Import/Export Audit Logs**
  - Build data serializations to export stock reports to CSV/JSON format.
- **Milestone 5: Interactive GUI Layout**
  - Develop visual layout panels showing item rarity color highlights.
## 4. Technical Stack
- **GUI**: `CustomTkinter`
- **Database**: `sqlite3`
- **Report generation**: `csv`, `json` modules

## 5. Specs: SQLite Database Schema & Transaction Models
To ensure data consistency and integrity, a structured SQLite database schema is designed.
- **Schema structure**:
  ```sql
  CREATE TABLE IF NOT EXISTS inventory_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      sku TEXT UNIQUE,
      category TEXT,
      rarity TEXT,
      quantity INTEGER DEFAULT 0,
      threshold INTEGER DEFAULT 5,
      price REAL
  );
  ```
  ```sql
  CREATE TABLE IF NOT EXISTS audit_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id INTEGER,
      change_type TEXT,
      quantity_delta INTEGER,
      timestamp INTEGER,
      FOREIGN KEY(item_id) REFERENCES inventory_items(id)
  );
  ```
- **ACID Transaction Safeguards**:
  - Database helper routines run inside explicit `WITH conn:` contexts.
  - Automatic rollbacks are executed on SQL errors to prevent partial modifications.

## 6. Specs: Search, Filtering, and Pagination Logic
Handling search queries over large inventories requires performant indices and SQL constraints.
- **Query Search Logic**:
  ```sql
  SELECT * FROM inventory_items 
  WHERE name LIKE :query OR sku LIKE :query
  ```
- **Multi-Level Filters**:
  - Search queries are combined dynamically:
    ```sql
    SELECT * FROM inventory_items 
    WHERE (name LIKE :query) AND rarity = :rarity AND quantity <= :quantity_limit
    ```
- **Cursor-Based Pagination**:
  - Displays maximum `50` items per page.
  - Uses `LIMIT 50 OFFSET :offset` clause to prevent system UI memory overhead.

## 7. Specs: Low Stock Alerts & Automated Notifications
To maintain operational efficiency, a threshold monitoring engine checks stock bounds.
- **Trigger condition**: Executed whenever quantity is decremented.
  `if quantity < threshold: trigger_alert()`
- **Notification Alert GUI**:
  - Changes background panel color to alert crimson: `#EF4444`.
  - Displays text badge: "CRITICAL: STOCK LOW".
- **Auto-Restock Request Generator**:
  - Spawns draft purchase request files in CSV format inside `restock_requests/` directory containing item details and replenishment order targets.

## 8. Specs: Data Import/Export & Report Generation
To interface with external systems, modular serialization handlers are defined.
- **Export format standard**: UTF-8 encoded CSV reporting.
- **Import Validation Steps**:
  - Prior to appending CSV contents, database records verify header presence and integrity.
  - Incorrect rows are flagged, logged to `import_errors.log`, and skipped.
