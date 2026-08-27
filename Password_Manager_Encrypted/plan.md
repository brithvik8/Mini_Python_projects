# Project Plan: Encrypted Password Manager with Secure Vault

## 1. Project Overview
A highly secure, offline password manager featuring Master Password entry, cryptographic key derivation, AES-256 database encryption, password generators, and categorizations.

## 2. General Requirements
- Language: Python 3.12+
- Platform: Cross-platform (Windows/macOS/Linux)
- Database: Local SQLite
- Cryptography: PBKDF2HMAC key derivation with AES-256 encryption

## 3. Development Milestones
- **Milestone 1: Cryptographic Service**
  - Implement PBKDF2HMAC key derivation.
  - Implement AES-256 symmetric encryption and decryption.
- **Milestone 2: Database Layer**
  - Design schema for encrypted credentials store.
  - Write CRUD operations with SQL parameters (prevent SQL injection).
- **Milestone 3: UI Design Layout**
  - Build Auth Login window and Dashboard layout.
- **Milestone 4: Search & Clipboard Integration**
  - Implement search logic, clipboard copy, and auto-clear timer.
- **Milestone 5: Security Lockout & Release Packaging**
  - Build lockout system and compile using PyInstaller.

## 4. Technical Stack
- **GUI Framework**: `CustomTkinter`
- **Database**: `sqlite3`
- **Crypto Library**: `cryptography`
- **Clipboard Utility**: `pyperclip`

## 5. Database Schema Structure
- `config` table:
  - `id` (INTEGER PRIMARY KEY)
  - `salt` (BLOB) - Salt used for PBKDF2HMAC
  - `verifier` (BLOB) - Encrypted verification token to check master password
- `credentials` table:
  - `id` (INTEGER PRIMARY KEY)
  - `site_name` (TEXT)
  - `username` (TEXT)
  - `encrypted_password` (BLOB)
  - `category` (TEXT)
  - `created_at` (TIMESTAMP)

## 6. UI/UX Style Guide
- **Branding Color Palette**:
  - Background: Cyber Black (`#0B0F19`)
  - Primary Accent: Cobalt Blue (`#2563EB`)
  - Alerts/Warning: Crimson Red (`#EF4444`)
- **Key Interface Views**:
  - **Auth Window**: Minimalist login form with password show/hide button and validation indicator.
  - **Vault Window**: Left-aligned navigation panel for quick search filters and right-pane credentials table showing copyable text boxes.

## 7. Security Architecture & Threat Vectors
- **Zero-Knowledge Design**: The derived decryption key is never stored locally on disk. It is stored solely in memory while the application session is active and wiped immediately on exit.
- **Brute Force Defense**: The master login attempts are validated against a local lockout limit. If exceeded, a progressive delay (e.g. 5s, 10s, 30s) is enforced before processing the next attempt.
- **Clipboard Auto-Clear**: Copied credentials are automatically cleared from the operating system's clipboard memory after 30 seconds using a background thread observer.

## 8. Extended Specs: Cryptographic Engine & Salt/Key Derivation Security (Day 11)
To strengthen password storage protection, PBKDF2HMAC is configured with strict iterations.
- **Key derivation scheme**: Uses PBKDF2 with SHA-256 hash.
- **Cryptographic Strength Parameters**:
  - Iterations count: `600,000` cycles.
  - Salt size: `16` bytes (randomly generated using `os.urandom`).
- **Decryption verifier check**:
  - Derives verifier hash during login to validate correctness without decrypting credentials.

## 9. Extended Specs: Database Encryption Layer & Secure SQL Queries (Day 12)
Each stored credential is encrypted individually before SQL execution.
- **AES-256 encryption standard**: CBC mode with randomized initialization vector (IV) of `16` bytes.
- **Ciphertext format**:
  - The payload stored in SQLite BLOB contains:
    `IV (16 bytes) + Encrypted Ciphertext`
