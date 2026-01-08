"""
Authentication Utilities for Streamlit Pages

This module provides decorators and functions to handle user authentication
checks across different pages of the Streamlit application.
"""

import streamlit as st
from functools import wraps

def require_authentication(func):
    """
    Decorator to ensure a user is authenticated before accessing a page.

    If the user is not authenticated, they are shown a warning and redirected
    to the main login page.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.warning("🔒 Please log in to access this page.")
            st.switch_page("main.py")
            return
        return func(*args, **kwargs)
    return wrapper
