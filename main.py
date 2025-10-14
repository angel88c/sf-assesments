"""
Main Application Module

This module serves as the entry point for the iBtest Assessment application.
It sets up the environment and redirects to the default assessment page.

Refactored to use new architecture with:
- Centralized configuration
- Separated authentication logic
- Improved error handling
"""

import streamlit as st
from core.auth import AuthService
from core.logging_config import setup_logging, get_logger
from pages.utils.global_styles import set_global_styles

# Setup logging
setup_logging(log_level="INFO")
logger = get_logger(__name__)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    
if 'target_page' not in st.session_state:
    # Get target page from URL
    url_params = st.query_params
    st.session_state.target_page = url_params.get("page", ["ict_assessment"])


# Apply global styles
set_global_styles()


def main():
    """Main application entry point."""
    logger.info("Starting iBtest Assessment Application")
    
    # Create authentication service
    auth_service = AuthService()
    
    if not auth_service.is_authenticated():
        logger.debug("User not authenticated, showing login form")
        auth_service.render_login_form()
    else:
        logger.debug("User authenticated, redirecting to target page")
        
        # Get target page
        if isinstance(st.session_state.target_page, list):
            target_page = st.session_state.target_page[0]        
        else:
            target_page = st.session_state.target_page
        
        logger.info(f"Redirecting to page: {target_page}")
        
        # Route to appropriate assessment page
        page_routes = {
            "ict_assessment": "pages/ict_assessment.py",
            "iat_assessment": "pages/iat_assessment.py",
            "fct_assessment": "pages/fct_assessment.py"
        }
        
        page_path = page_routes.get(target_page, "pages/ict_assessment.py")
        st.switch_page(page_path)


if __name__ == "__main__":
    main()
