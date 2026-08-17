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
