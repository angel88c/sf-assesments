"""
Settings Module

Centralized configuration management using environment variables.
This module provides a single source of truth for all application settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


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
    def load_from_env(cls, env_path: Optional[Path] = None) -> 'Settings':
        """
        Load settings from environment variables.
        
        Args:
            env_path: Optional path to .env file. If None, searches in parent directories.
            
        Returns:
            Settings instance with all configuration loaded.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
        # Load .env file
        if env_path is None:
            env_path = Path(__file__).parent.parent / ".env"
        
        load_dotenv(env_path, override=True)
        
        # Validate and load Salesforce config
        salesforce = SalesforceConfig(
            username=cls._get_required_env('SALESFORCE_USERNAME'),
            password=cls._get_required_env('SALESFORCE_PASSWORD'),
            security_token=cls._get_required_env('SALESFORCE_SECURITY_TOKEN'),
            consumer_key=cls._get_required_env('SALESFORCE_CONSUMER_KEY'),
            consumer_secret=cls._get_required_env('SALESFORCE_CONSUMER_SECRET'),
            token_url=os.getenv('TOKEN_URL', 'https://login.salesforce.com/services/oauth2/token'),
            timeout=int(os.getenv('SF_TIMEOUT', '30'))
        )
        
        # Validate and load Storage config
        storage = StorageConfig(
            base_path=Path(cls._get_required_env('PATH_FILE')),
            sharepoint_path=cls._get_required_env('PATH_TO_SHAREPOINT'),
            template_ict=Path(cls._get_required_env('TEMPLATE_ICT')),
            template_fct=Path(cls._get_required_env('TEMPLATE_FCT')),
            template_iat=Path(cls._get_required_env('TEMPLATE_IAT')),
            provider=os.getenv('STORAGE_PROVIDER', 'local')
        )
        
        # Validate and load Auth config
        auth = AuthConfig(
            password_hash=cls._get_required_env('APP_PASSWORD')
        )
        
        # Load Azure config (optional, only needed for SharePoint)
        azure = None
        sharepoint = None
        if storage.provider.lower() == 'sharepoint':
            azure = AzureConfig(
                tenant_id=cls._get_required_env('AZURE_TENANT_ID'),
                client_id=cls._get_required_env('AZURE_CLIENT_ID'),
                client_secret=cls._get_required_env('AZURE_CLIENT_SECRET')
            )
            sharepoint = SharePointConfig(
                site_id=cls._get_required_env('SHAREPOINT_SITE_ID'),
                drive_id=cls._get_required_env('SHAREPOINT_DRIVE_ID')
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
