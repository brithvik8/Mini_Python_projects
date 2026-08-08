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
