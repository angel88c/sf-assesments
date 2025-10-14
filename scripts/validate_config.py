#!/usr/bin/env python3
"""
Configuration Validation Script

This script validates that all required environment variables are properly
configured and that the application can start successfully.

Usage:
    python scripts/validate_config.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def validate_configuration():
    """Validate application configuration."""
    print("🔍 Validating iBtest Assessment Configuration...\n")
    
    errors = []
    warnings = []
    
    # Test 1: Load configuration
    print("1. Loading configuration from .env file...")
    try:
        from config import get_settings
        settings = get_settings()
        print("   ✅ Configuration loaded successfully\n")
    except ValueError as e:
        print(f"   ❌ Configuration error: {e}\n")
        errors.append(str(e))
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}\n")
        errors.append(str(e))
        return False
    
    # Test 2: Validate Salesforce configuration
    print("2. Validating Salesforce configuration...")
    try:
        sf_config = settings.salesforce
        print(f"   ✅ Username: {sf_config.username}")
        print(f"   ✅ Token URL: {sf_config.token_url}")
        print(f"   ✅ Timeout: {sf_config.timeout}s")
        print(f"   ✅ Consumer Key: {sf_config.consumer_key[:10]}...")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        errors.append(f"Salesforce config: {e}")
    
    # Test 3: Validate Storage configuration
    print("3. Validating Storage configuration...")
    try:
        storage_config = settings.storage
        
        # Check base path
        if storage_config.base_path.exists():
            print(f"   ✅ Base path exists: {storage_config.base_path}")
        else:
            print(f"   ⚠️  Base path does not exist: {storage_config.base_path}")
            warnings.append(f"Base path not found: {storage_config.base_path}")
        
        # Check templates
        templates = {
            "ICT": storage_config.template_ict,
            "FCT": storage_config.template_fct,
            "IAT": storage_config.template_iat
        }
        
        for name, path in templates.items():
            if path.exists():
                print(f"   ✅ {name} template exists: {path}")
            else:
                print(f"   ⚠️  {name} template not found: {path}")
                warnings.append(f"{name} template not found: {path}")
        
        print(f"   ✅ SharePoint path: {storage_config.sharepoint_path}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        errors.append(f"Storage config: {e}")
    
    # Test 4: Validate Authentication configuration
    print("4. Validating Authentication configuration...")
    try:
        auth_config = settings.auth
        if len(auth_config.password_hash) == 64:  # SHA-256 produces 64 hex chars
            print(f"   ✅ Password hash configured (SHA-256)")
        else:
            print(f"   ⚠️  Password hash length unexpected: {len(auth_config.password_hash)}")
            warnings.append("Password hash might not be SHA-256")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        errors.append(f"Auth config: {e}")
    
    # Test 5: Test Salesforce connection (optional)
    print("5. Testing Salesforce connection...")
    try:
        from services.salesforce_service import SalesforceService
        sf_service = SalesforceService()
        print("   ✅ Salesforce service initialized")
        
        # Try to get accounts
        accounts = sf_service.get_accounts()
        print(f"   ✅ Successfully retrieved {len(accounts)} accounts")
        print()
    except Exception as e:
        print(f"   ⚠️  Could not connect to Salesforce: {e}")
        print("   ℹ️  This might be expected in development environment")
        warnings.append(f"Salesforce connection: {e}")
        print()
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    if errors:
        print(f"\n❌ {len(errors)} ERROR(S) FOUND:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    if not errors and not warnings:
        print("\n✅ All validations passed successfully!")
        print("   Your configuration is ready to use.")
    elif not errors:
        print("\n✅ Configuration is valid with some warnings.")
        print("   The application should work, but check warnings above.")
    else:
        print("\n❌ Configuration has errors that must be fixed.")
        print("   Please update your .env file and try again.")
    
    print("="*70 + "\n")
    
    return len(errors) == 0


def main():
    """Main entry point."""
    try:
        success = validate_configuration()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
