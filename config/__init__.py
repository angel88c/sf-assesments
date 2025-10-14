"""
Configuration Package

This package contains configuration management for the iBtest Assessment application.
"""

from .settings import Settings, get_settings

__all__ = ['Settings', 'get_settings']
