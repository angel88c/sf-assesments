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
    def _get_config_value(cls, key: str, section: Optional[str] = None, default: Any = None) -> Any:
        """
        Get configuration value from st.secrets (Streamlit Cloud) or environment variables (local).
        
        Args:
            key: Configuration key name.
            section: Optional section name for st.secrets (e.g., 'salesforce').
            default: Default value if not found.
            
        Returns:
            Configuration value.
        """
        if cls._is_streamlit_cloud():
            # Running on Streamlit Cloud - use st.secrets
            try:
                if section:
                    return st.secrets[section][key]
                else:
                    return st.secrets[key]
            except (KeyError, AttributeError):
                if default is not None:
                    return default
                raise ValueError(f"Required secret '{section}.{key if section else key}' not found in st.secrets")
        else:
            # Running locally - use environment variables
            value = os.getenv(key.upper() if not section else f"{section.upper()}_{key.upper()}", default)
            if value is None and default is None:
                # Try without section prefix
                value = os.getenv(key.upper(), default)
            return value
    
    @classmethod
    def load_from_env(cls, env_path: Optional[Path] = None) -> 'Settings':
        """
        Load settings from environment variables or Streamlit secrets.
        
        Automatically detects the environment:
        - Streamlit Cloud: Reads from st.secrets (secrets.toml)
        - Local development: Reads from .env file
        
        Args:
            env_path: Optional path to .env file. If None, searches in parent directories.
            
        Returns:
            Settings instance with all configuration loaded.
            
        Raises:
            ValueError: If required configuration values are missing.
        """
        # Load .env file only if running locally
        if not cls._is_streamlit_cloud():
            if env_path is None:
                env_path = Path(__file__).parent.parent / ".env"
            load_dotenv(env_path, override=True)
        
        # Detect environment
        is_cloud = cls._is_streamlit_cloud()
        
        # Validate and load Salesforce config
        salesforce = SalesforceConfig(
            username=cls._get_config_value('username', 'salesforce') if is_cloud else cls._get_required_env('SALESFORCE_USERNAME'),
            password=cls._get_config_value('password', 'salesforce') if is_cloud else cls._get_required_env('SALESFORCE_PASSWORD'),
            security_token=cls._get_config_value('security_token', 'salesforce') if is_cloud else cls._get_required_env('SALESFORCE_SECURITY_TOKEN'),
            consumer_key=cls._get_config_value('consumer_key', 'salesforce') if is_cloud else cls._get_required_env('SALESFORCE_CONSUMER_KEY'),
            consumer_secret=cls._get_config_value('consumer_secret', 'salesforce') if is_cloud else cls._get_required_env('SALESFORCE_CONSUMER_SECRET'),
            token_url=cls._get_config_value('token_url', 'salesforce', 'https://login.salesforce.com/services/oauth2/token'),
            timeout=int(cls._get_config_value('timeout', 'salesforce', 40))
        )
        
        # Validate and load Storage config
        storage = StorageConfig(
            base_path=Path(cls._get_config_value('path_file', 'storage') if is_cloud else cls._get_required_env('PATH_FILE')),
            sharepoint_path=cls._get_config_value('path_to_sharepoint', 'storage') if is_cloud else cls._get_required_env('PATH_TO_SHAREPOINT'),
            template_ict=Path(cls._get_config_value('template_ict', 'storage') if is_cloud else cls._get_required_env('TEMPLATE_ICT')),
            template_fct=Path(cls._get_config_value('template_fct', 'storage') if is_cloud else cls._get_required_env('TEMPLATE_FCT')),
            template_iat=Path(cls._get_config_value('template_iat', 'storage') if is_cloud else cls._get_required_env('TEMPLATE_IAT')),
            provider=cls._get_config_value('provider', 'storage', 'local')
        )
        
        # Validate and load Auth config
        auth = AuthConfig(
            password_hash=cls._get_config_value('password_hash', 'auth') if is_cloud else cls._get_required_env('APP_PASSWORD')
        )
        
        # Load Azure and SharePoint config (optional, only needed for SharePoint)
        azure = None
        sharepoint = None
        if storage.provider.lower() == 'sharepoint':
            if is_cloud:
                azure = AzureConfig(
                    tenant_id=cls._get_config_value('tenant_id', 'sharepoint'),
                    client_id=cls._get_config_value('client_id', 'sharepoint'),
                    client_secret=cls._get_config_value('client_secret', 'sharepoint')
                )
                sharepoint = SharePointConfig(
                    site_id=cls._get_config_value('site_id', 'sharepoint'),
                    drive_id=cls._get_config_value('drive_id', 'sharepoint'),
                    base_path=cls._get_config_value('base_path', 'sharepoint', '')
                )
            else:
                azure = AzureConfig(
                    tenant_id=cls._get_required_env('AZURE_TENANT_ID'),
                    client_id=cls._get_required_env('AZURE_CLIENT_ID'),
                    client_secret=cls._get_required_env('AZURE_CLIENT_SECRET')
                )
                sharepoint = SharePointConfig(
                    site_id=cls._get_required_env('SHAREPOINT_SITE_ID'),
                    drive_id=cls._get_required_env('SHAREPOINT_DRIVE_ID'),
                    base_path=os.getenv('SHAREPOINT_BASE_PATH', '')
                )
        
        return cls(
            salesforce=salesforce,
            storage=storage,
            auth=auth,
            azure=azure,
            sharepoint=sharepoint
        )
    
    @staticmethod
    def _get_required_env(key: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            key: Environment variable name.
            
        Returns:
            Environment variable value.
            
        Raises:
            ValueError: If the environment variable is not set.
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value


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
