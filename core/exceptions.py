"""
Custom Exceptions Module

This module defines custom exceptions for the iBtest Assessment application.
Using custom exceptions improves error handling and makes debugging easier.
"""


class IBTestError(Exception):
    """Base exception for all iBtest application errors."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize the exception.
        
        Args:
            message: Error message.
            details: Optional dictionary with additional error details.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(IBTestError):
    """Exception raised for authentication errors."""
    pass


class ValidationError(IBTestError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message.
            field: Name of the field that failed validation.
            details: Optional dictionary with additional error details.
        """
        super().__init__(message, details)
        self.field = field


class SalesforceError(IBTestError):
    """Exception raised for Salesforce API errors."""
    pass


class StorageError(IBTestError):
    """Exception raised for file storage errors."""
    pass


class ConfigurationError(IBTestError):
    """Exception raised for configuration errors."""
    pass
