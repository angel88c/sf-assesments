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

def initialize_session_state():
    """Initializes the session state for the application."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if 'target_page' not in st.session_state:
        url_params = st.query_params
        st.session_state.target_page = url_params.get("page", "ict_assessment")

def get_target_page() -> str:
    """Retrieves the target page from the session state."""
    target = st.session_state.get('target_page', 'ict_assessment')
    # query_params can return a list, so we take the first element
    return target[0] if isinstance(target, list) else target

def main():
    """Main application entry point."""
    try:
        logger.info("Starting iBtest Assessment Application")

        initialize_session_state()
        set_global_styles()

        auth_service = AuthService()

        if not auth_service.is_authenticated():
            logger.debug("User not authenticated, showing login form")
            auth_service.render_login_form()
            return

        logger.debug("User authenticated, redirecting to target page")
        
        target_page = get_target_page()
        logger.info(f"Redirecting to page: {target_page}")

        page_routes = {
            "ict_assessment": "pages/ict_assessment.py",
            "iat_assessment": "pages/iat_assessment.py",
            "fct_assessment": "pages/fct_assessment.py"
        }

        page_path = page_routes.get(target_page, "pages/ict_assessment.py")
        st.switch_page(page_path)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
        st.error("An unexpected error occurred. Please contact support.")


if __name__ == "__main__":
    main()
