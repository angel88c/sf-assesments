"""
Logging Configuration Module

This module provides centralized logging configuration for the iBtest Assessment application.
It sets up structured logging with appropriate formatters and handlers.

Environment-aware logging:
- Development (local): INFO level - Detailed logs
- Production (Streamlit Cloud): WARNING level - Only important messages
"""

import logging
import sys
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

# Try to import streamlit to detect cloud environment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


def _is_production() -> bool:
    """
    Detect if running in production (Streamlit Cloud).
    
    Returns:
        True if in production, False if in development.
    """
    # Check if running on Streamlit Cloud
    if HAS_STREAMLIT and hasattr(st, 'secrets') and len(st.secrets) > 0:
        return True
    
    # Check environment variable
    if os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud':
        return True
    
    return False


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[Path] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Set up logging configuration for the application.
    
    Automatically adjusts log level based on environment:
    - Development (local): INFO level - Detailed logs for debugging
    - Production (Streamlit Cloud): WARNING level - Only important messages
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   If None, automatically determined based on environment.
        log_file: Optional path to log file. If None, logs only to console.
        log_format: Optional custom log format string.
    """
    # Auto-detect log level based on environment if not specified
    if log_level is None:
        log_level = "WARNING" if _is_production() else "INFO"
    if log_format is None:
        log_format = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'
        )
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Name for the logger (usually __name__ of the module).
        
    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class to add logging functionality to any class.
    
    Usage:
        class MyClass(LoggerMixin):
            def my_method(self):
                self.logger.info("This is a log message")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)
