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
