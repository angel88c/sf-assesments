#!/usr/bin/env python3
"""
Password Hash Generator

This script helps generate SHA-256 password hashes for the APP_PASSWORD
environment variable.

Usage:
    python scripts/generate_password_hash.py
"""

import hashlib
import getpass


def generate_hash(password: str) -> str:
    """Generate SHA-256 hash of password."""
    return hashlib.sha256(password.encode()).hexdigest()


def main():
    """Main entry point."""
    print("="*70)
    print("PASSWORD HASH GENERATOR")
    print("="*70)
    print("\nThis tool will generate a SHA-256 hash for your application password.")
    print("Use this hash in your .env file for APP_PASSWORD variable.\n")
    
    # Get password from user
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    
    # Validate passwords match
    if password != password_confirm:
        print("\n❌ Passwords do not match. Please try again.")
        return
    
    # Validate password is not empty
    if not password:
        print("\n❌ Password cannot be empty.")
        return
    
    # Generate hash
    password_hash = generate_hash(password)
    
    # Display result
    print("\n" + "="*70)
    print("✅ PASSWORD HASH GENERATED")
    print("="*70)
    print(f"\nHash: {password_hash}")
    print("\nAdd this line to your .env file:")
    print(f"APP_PASSWORD={password_hash}")
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
