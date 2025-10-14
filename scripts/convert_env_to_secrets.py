#!/usr/bin/env python3
"""
Convert .env file to Streamlit secrets.toml format

This script reads your .env file and generates a secrets.toml file
with the same values in the correct format for Streamlit Cloud.

Usage:
    python scripts/convert_env_to_secrets.py
"""

import os
from pathlib import Path
from dotenv import dotenv_values

def main():
    """Convert .env to secrets.toml"""
    
    # Paths
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    secrets_file = project_root / ".streamlit" / "secrets.toml"
    
    # Check if .env exists
    if not env_file.exists():
        print(f"❌ Error: .env file not found at {env_file}")
        print("Please create a .env file first.")
        return 1
    
    # Load .env
    print(f"📖 Reading {env_file}")
    env_vars = dotenv_values(env_file)
    
    # Create .streamlit folder if it doesn't exist
    secrets_file.parent.mkdir(exist_ok=True)
    
    # Generate secrets.toml content
    secrets_content = generate_secrets_toml(env_vars)
    
    # Write to file
    print(f"✍️  Writing to {secrets_file}")
    with open(secrets_file, 'w') as f:
        f.write(secrets_content)
    
    print(f"✅ Successfully created {secrets_file}")
    print("\n⚠️  IMPORTANT:")
    print("1. Review the generated file for accuracy")
    print("2. This file is ignored by Git (.gitignore)")
    print("3. Copy the content to Streamlit Cloud Secrets dashboard when deploying")
    print("\n📋 Next steps:")
    print("   - Review: nano .streamlit/secrets.toml")
    print("   - Deploy: https://share.streamlit.io/")
    
    return 0


def generate_secrets_toml(env_vars: dict) -> str:
    """Generate secrets.toml content from env vars"""
    
    content = [
        "# Streamlit Cloud Secrets Configuration",
        "# Generated from .env file",
        "# ",
        "# ⚠️  IMPORTANT:",
        "# - Review all values before using",
        "# - Never commit this file to Git",
        "# - Use this for Streamlit Cloud deployment",
        "",
        "# ============================================================================",
        "# SALESFORCE CONFIGURATION",
        "# ============================================================================",
        "[salesforce]",
        f'username = "{env_vars.get("SALESFORCE_USERNAME", "")}"',
        f'password = "{env_vars.get("SALESFORCE_PASSWORD", "")}"',
        f'security_token = "{env_vars.get("SALESFORCE_SECURITY_TOKEN", "")}"',
        f'consumer_key = "{env_vars.get("SALESFORCE_CONSUMER_KEY", "")}"',
        f'consumer_secret = "{env_vars.get("SALESFORCE_CONSUMER_SECRET", "")}"',
        f'token_url = "{env_vars.get("TOKEN_URL", "https://login.salesforce.com/services/oauth2/token")}"',
        f'timeout = {env_vars.get("SF_TIMEOUT", "40")}',
        "",
        "# ============================================================================",
        "# STORAGE CONFIGURATION",
        "# ============================================================================",
        "[storage]",
        f'provider = "{env_vars.get("STORAGE_PROVIDER", "local")}"',
        f'path_file = "{env_vars.get("PATH_FILE", "/tmp")}"',
        f'path_to_sharepoint = "{env_vars.get("PATH_TO_SHAREPOINT", "")}"',
        f'template_ict = "{env_vars.get("TEMPLATE_ICT", "/tmp/TEMPLATE_ICT")}"',
        f'template_fct = "{env_vars.get("TEMPLATE_FCT", "/tmp/TEMPLATE_FCT")}"',
        f'template_iat = "{env_vars.get("TEMPLATE_IAT", "/tmp/TEMPLATE_IAT")}"',
        "",
        "# ============================================================================",
        "# SHAREPOINT CONFIGURATION",
        "# ============================================================================",
        "[sharepoint]",
        f'base_path = "{env_vars.get("SHAREPOINT_BASE_PATH", "")}"',
        f'tenant_id = "{env_vars.get("AZURE_TENANT_ID", "")}"',
        f'client_id = "{env_vars.get("AZURE_CLIENT_ID", "")}"',
        f'client_secret = "{env_vars.get("AZURE_CLIENT_SECRET", "")}"',
        f'site_id = "{env_vars.get("SHAREPOINT_SITE_ID", "")}"',
        f'drive_id = "{env_vars.get("SHAREPOINT_DRIVE_ID", "")}"',
        "",
        "# ============================================================================",
        "# AUTHENTICATION",
        "# ============================================================================",
        "[auth]",
        f'password_hash = "{env_vars.get("APP_PASSWORD", "")}"',
        "",
        "# ============================================================================",
        "# OPTIONAL CONFIGURATION",
        "# ============================================================================",
        "[logging]",
        f'level = "{env_vars.get("LOG_LEVEL", "INFO")}"',
        "# file = \"/path/to/logs/app.log\"  # Optional",
        ""
    ]
    
    return "\n".join(content)


if __name__ == "__main__":
    exit(main())
