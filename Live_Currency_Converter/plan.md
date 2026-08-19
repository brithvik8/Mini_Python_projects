# Project Plan: Live Currency Converter with Historical Charts

## 1. Project Overview
A responsive desktop currency converter application that pulls real-time exchange rates from a public API, performs high-precision currency conversions, stores rates locally for offline operations, and displays historical exchange rate trend graphs.

## 2. General Requirements
- Language: Python 3.12+
- Platform: Cross-platform (Windows/macOS/Linux)
- Storage: Local SQLite database for offline rate caching and historical trend logging.
- External APIs: Exchangerate.host or ExchangeRate-API (fallback).
## 3. Development Milestones
- **Milestone 1: Exchange Rate API Integration**
  - Integrate requests handler for exchange rate APIs with validation.
- **Milestone 2: Database Storage & Caching Layer**
  - Design SQL schema for caching rates and logging historical data.
- **Milestone 3: Core Conversion Logic Engine**
  - Write high-precision conversion calculation math supporting multiple decimal precision configurations.
- **Milestone 4: Modern GUI & Interactivity**
  - Construct UI using CustomTkinter with search capabilities.
- **Milestone 5: Matplotlib Visualization Charts**
  - Integrate trend charts visualizing currency rate shifts over 7, 30, and 90 days.
## 4. Technical Stack
- **GUI**: `CustomTkinter`
- **HTTP Client**: `requests`
- **Plotting/Charts**: `matplotlib`
- **Database**: `sqlite3`

## 5. Specs: API Integration & Request Caching
To fetch real-time conversion rates without hitting rate limits, a secure API connection manager is established.
- **Endpoint Structure**: Requests are formatted dynamically:
  `https://open.er-api.com/v6/latest/{BASE_CURRENCY}`
- **HTTP Exception Handling**:
  - Timeout limit: `5.0` seconds.
  - Retries: Progressive backoff retry handler (1s, 2s, 4s) up to 3 times before loading cached rates from SQLite.
- **Cache Expiry Model**:
  - Fetch payload includes standard metadata field `time_next_update_unix`.
  - Local checks verify if `current_time_unix >= time_next_update_unix` to avoid redundant API queries.

## 6. Specs: Offline Fallback & Historical Data Store
A robust local SQLite database is utilized to ensure functionality when internet connection is lost.
- **Database schema**:
  ```sql
  CREATE TABLE IF NOT EXISTS exchange_rates (
      base TEXT,
      target TEXT,
      rate REAL,
      last_updated INTEGER,
      PRIMARY KEY (base, target)
  );
  ```
  ```sql
  CREATE TABLE IF NOT EXISTS rate_history (
      base TEXT,
      target TEXT,
      rate REAL,
      timestamp INTEGER
  );
  ```
- **Offline Warning Indicators**:
  - If network check fails, the GUI changes state:
    - Status label displays: "Offline Mode — Using Cached Rates from {last_updated}".
    - Search entry fields remain interactive with local SQLite lookup.

## 7. Specs: Multi-Currency Conversion Logic & Precision Handling
To prevent float inaccuracies in monetary mathematics, a strict numerical precision engine is implemented.
- **Precision Standard**: Uses Python's native `decimal.Decimal` module for all financial operations.
- **Decimal Precision Settings**:
  - Default precision setting: `4` decimal places (e.g. 1.1234).
  - Extended precision setting: Up to `8` decimal places for cryptocurrencies or low-value pairs.
