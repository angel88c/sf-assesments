"""
Core Package

This package contains core functionality for the iBtest Assessment application.
"""

from .auth import AuthService
from .exceptions import (
    IBTestError,
    AuthenticationError,
    ValidationError,
    SalesforceError,
    StorageError
)
from .logging_config import setup_logging, get_logger

__all__ = [
    'AuthService',
    'IBTestError',
    'AuthenticationError',
    'ValidationError',
    'SalesforceError',
    'StorageError',
    'setup_logging',
    'get_logger'
]
