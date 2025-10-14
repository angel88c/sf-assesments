"""
Storage Package

This package provides an abstraction layer for file storage operations.
It allows easy switching between different storage backends (local, SharePoint, etc.).
"""

from .base import StorageProvider
from .local_storage import LocalStorageProvider
from .sharepoint_storage import SharePointStorageProvider

__all__ = ['StorageProvider', 'LocalStorageProvider', 'SharePointStorageProvider']
