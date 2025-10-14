"""
Authentication Module

This module provides authentication functionality for the iBtest Assessment application.
It separates authentication logic from the main application flow.
"""

import re
import hashlib
import streamlit as st
from functools import wraps
from typing import Optional
from .exceptions import AuthenticationError
from config import get_settings


class AuthService:
    """
    Service for handling user authentication.
    
    This class encapsulates all authentication logic, making it easier to test
    and maintain.
    """
    
    def __init__(self):
        """Initialize the authentication service."""
        self.settings = get_settings()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password.
            
        Returns:
            Hashed password as hexadecimal string.
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate.
            
        Returns:
            True if email format is valid, False otherwise.
        """
        if not email:
            return False
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    
    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address.
            password: User's password.
            
        Returns:
            True if authentication successful, False otherwise.
            
        Raises:
            AuthenticationError: If email format is invalid.
        """
        # Validate email format
        if not self.is_valid_email(email):
            raise AuthenticationError("Invalid email format")
        
        # Hash the provided password
        entered_password_hash = self.hash_password(password)
        
        # Compare with stored hash
        return entered_password_hash == self.settings.auth.password_hash
    
    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if the current user is authenticated.
        
        Returns:
            True if user is authenticated, False otherwise.
        """
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def login(email: str) -> None:
        """
        Mark the current session as authenticated.
        
        Args:
            email: Authenticated user's email.
        """
        st.session_state['authenticated'] = True
        st.session_state['user_email'] = email
    
    @staticmethod
    def logout() -> None:
        """Log out the current user."""
        st.session_state['authenticated'] = False
        if 'user_email' in st.session_state:
            del st.session_state['user_email']
    
    def render_login_form(self) -> None:
        """
        Render the login form in Streamlit.
        
        This method handles the complete login flow including form rendering
        and authentication.
        """
        with st.form("login_form"):
            st.header("Login")
            
            email = st.text_input(
                "Email",
                type="default",
                placeholder="Enter provided email",
                value="customer@ibtest.com"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter provided password"
            )
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                try:
                    if self.authenticate(email, password):
                        self.login(email)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                except AuthenticationError as e:
                    st.error(str(e))


def require_authentication(func):
    """
    Decorator to require authentication for a page.
    
    This decorator checks if the user is authenticated before allowing access
    to a page. If not authenticated, it redirects to the login page.
    
    Usage:
        @require_authentication
        def my_protected_page():
            # Page content
            pass
    
    Args:
        func: Function to decorate.
        
    Returns:
        Wrapped function that checks authentication.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not AuthService.is_authenticated():
            st.warning("Please log in to access this page")
            st.switch_page("main.py")
            return None
        return func(*args, **kwargs)
    
    return wrapper
