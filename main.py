"""
Main Application Module

This module serves as the entry point for the iBtest Assessment application.
It sets up the environment and redirects to the default assessment page.
"""

import os
import streamlit as st
import re
from dotenv import load_dotenv
import hashlib
from urllib.parse import urlparse, parse_qs
from pages.utils.global_styles import set_global_styles

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    
if 'target_page' not in st.session_state:
    # Get target page from URL
    url_params = st.query_params
    st.session_state.target_page = url_params.get("page", ["ict_assessment"])
    print(st.session_state.target_page)
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def login_form():
    with st.form("login_form"):
        email = st.text_input("Email", type="default", placeholder="Enter provided email")
        password = st.text_input("Password", type="password", placeholder="Enter provided password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not is_valid_email(email):
                st.error("Please enter a valid email and password")
                return False
        
            stored_password_hash = os.getenv("APP_PASSWORD")
            entered_password_hash = hash_password(password)
            
            if stored_password_hash and entered_password_hash == stored_password_hash:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Incorrect password")
                return False
        
    return True
                

# Set page configuration
# st.set_page_config(
#     page_title="iBtest Assessment",
#     page_icon="🔍",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )
set_global_styles()
def main():
    if not st.session_state['authenticated']:
        login_form()
    else:
        target_page = st.session_state.target_page
        if type(st.session_state.target_page) == list:
            target_page = st.session_state.target_page[0]        
            
        if target_page == "ICT_ASSESSMENT":
            st.switch_page("pages/ict_assessment.py")
        elif target_page == "IAT_ASSESSMENT":
            st.switch_page("pages/iat_assessment.py")
        elif target_page == "FCT_ASSESSMENT":
            st.switch_page("pages/fct_assessment.py")
        else:
            st.switch_page("pages/ict_assessment.py")

if __name__ == "__main__":
    main()
