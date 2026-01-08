"""
Settings Module

Centralized configuration management using environment variables.
This module provides a single source of truth for all application settings.

Supports both:
- Local development: Uses .env file
- Streamlit Cloud: Uses st.secrets from secrets.toml
"""

import os
from dataclasses import dataclass
from typing import Optional, Any
from pathlib import Path
from dotenv import load_dotenv

# Try to import streamlit for cloud deployment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


@dataclass
class SalesforceConfig:
    """Salesforce API configuration."""
    username: str
    password: str
    security_token: str
    consumer_key: str
    consumer_secret: str
    token_url: str
    timeout: int = 30


@dataclass
class StorageConfig:
    """File storage configuration."""
    base_path: Path
    sharepoint_path: str
    template_ict: Path
    template_fct: Path
    template_iat: Path
    provider: str = 'local'  # 'local' or 'sharepoint'


@dataclass
class AzureConfig:
    """Azure AD configuration for SharePoint."""
    tenant_id: str
    client_id: str
    client_secret: str


@dataclass
class SharePointConfig:
    """SharePoint configuration."""
    site_id: str
    drive_id: str
    base_path: str = ""  # Optional base path within SharePoint (e.g., "01_2025")


@dataclass
class AuthConfig:
    """Authentication configuration."""
    password_hash: str


@dataclass
class Settings:
    """
    Application settings loaded from environment variables.
    
    This class provides type-safe access to all configuration values.
    """
    salesforce: SalesforceConfig
    storage: StorageConfig
    auth: AuthConfig
    azure: Optional[AzureConfig] = None
    sharepoint: Optional[SharePointConfig] = None
    
    @classmethod
    def _is_streamlit_cloud(cls) -> bool:
        """Check if running on Streamlit Cloud."""
        return HAS_STREAMLIT and hasattr(st, 'secrets') and len(st.secrets) > 0

    @classmethod
    def _get_config_value(cls, key: str, section: Optional[str] = None, default: Any = None, required: bool = True) -> Any:
        """
        Get a configuration value from st.secrets or environment variables.
        Priority:
        1. Streamlit secrets (if on Streamlit Cloud or running with `streamlit run` locally)
        2. Environment variables
        """
        value = None
        # 1. Try Streamlit secrets
        if HAS_STREAMLIT and hasattr(st, 'secrets'):
            try:
                if section:
                    value = st.secrets[section][key]
                else:
                    value = st.secrets[key]
            except (KeyError, AttributeError):
                pass  # Not found in secrets, will try environment variables

        # 2. Try environment variables if not found in secrets
        if value is None:
            env_var_name = f"{section.upper()}_{key.upper()}" if section else key.upper()
            value = os.getenv(env_var_name)

        # 3. Use default if still not found
        if value is None:
            value = default

        # 4. Raise error if required and still not found
        if value is None and required and default is None:
            env_var_name = f"{section.upper()}_{key.upper()}" if section else key.upper()
            raise ValueError(f"Required configuration '{env_var_name}' not found in st.secrets or environment variables.")

        return value

    @classmethod
    def load_from_env(cls, env_path: Optional[Path] = None) -> 'Settings':
        """
        Load settings from environment variables or Streamlit secrets.
        """
        if not cls._is_streamlit_cloud():
            env_path = env_path or Path(__file__).parent.parent / ".env"
            if env_path.exists():
                load_dotenv(env_path, override=True)

        # Load Salesforce config
        salesforce = SalesforceConfig(
            username=cls._get_config_value('username', 'salesforce'),
            password=cls._get_config_value('password', 'salesforce'),
            security_token=cls._get_config_value('security_token', 'salesforce'),
            consumer_key=cls._get_config_value('consumer_key', 'salesforce'),
            consumer_secret=cls._get_config_value('consumer_secret', 'salesforce'),
            token_url=cls._get_config_value('token_url', 'salesforce', default='https://login.salesforce.com/services/oauth2/token'),
            timeout=int(cls._get_config_value('timeout', 'salesforce', default=40))
        )

        # Load Storage config
        storage = StorageConfig(
            base_path=Path(cls._get_config_value('path_file', 'storage')),
            sharepoint_path=cls._get_config_value('path_to_sharepoint', 'storage'),
            template_ict=Path(cls._get_config_value('template_ict', 'storage')),
            template_fct=Path(cls._get_config_value('template_fct', 'storage')),
            template_iat=Path(cls._get_config_value('template_iat', 'storage')),
            provider=cls._get_config_value('provider', 'storage', default='local')
        )

        # Load Auth config
        auth = AuthConfig(
            password_hash=cls._get_config_value('password_hash', section='auth', required=True)
        )

        # Load optional Azure and SharePoint config
        azure, sharepoint = None, None
        if storage.provider.lower() == 'sharepoint':
            azure = AzureConfig(
                tenant_id=cls._get_config_value('tenant_id', 'sharepoint'),
                client_id=cls._get_config_value('client_id', 'sharepoint'),
                client_secret=cls._get_config_value('client_secret', 'sharepoint')
            )
            sharepoint = SharePointConfig(
                site_id=cls._get_config_value('site_id', 'sharepoint'),
                drive_id=cls._get_config_value('drive_id', 'sharepoint'),
                base_path=cls._get_config_value('base_path', 'sharepoint', default='')
            )
            if sharepoint:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"✅ SharePoint config loaded - base_path: '{sharepoint.base_path}'")

        return cls(
            salesforce=salesforce,
            storage=storage,
            auth=auth,
            azure=azure,
            sharepoint=sharepoint
        )


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the application settings singleton.
    
    Returns:
        Settings instance.
    """
    global _settings
    if _settings is None:
        _settings = Settings.load_from_env()
    return _settings
