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
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    
if 'target_page' not in st.session_state:
    # Get target page from URL
    url_params = st.query_params
    st.session_state.target_page = url_params.get("page", ["ict_assessment"])
    
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def login_form():
    with st.form("login_form"):
        st.header("Login")
        email = st.text_input("Email", type="default", placeholder="Enter provided email", value="customer@ibtest.com")
        password = st.text_input("Password", type="password", placeholder="Enter provided password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            '''
            if not is_valid_email(email):
                st.error("Please enter a valid email and password")
                return False
            '''
            # Datos para la solicitud            
            payload = {
                "usr_name": email,
                "password": password 
            }
        
            # stored_password_hash = os.getenv("APP_PASSWORD")
            # entered_password_hash = stored_password_hash
            try:
                response = requests.post("http://localhost:35001/api/auth/signin", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['authenticated'] = True
                    st.session_state['token'] = data.get("token")  # Guardar el token en el store
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
                    return False                
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
                return False
            '''
            if stored_password_hash and entered_password_hash == stored_password_hash:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Incorrect password")
                return False
            '''
        
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
        
        if type(st.session_state.target_page) == list:
            target_page = st.session_state.target_page[0]        
        else:
            target_page = st.session_state.target_page
        
        print(target_page)
        if target_page == "ict_assessment":
            st.switch_page("pages/ict_assessment.py")
        elif target_page == "iat_assessment":
            st.switch_page("pages/iat_assessment.py")
        elif target_page == "fct_assessment":
            st.switch_page("pages/fct_assessment.py")
        elif target_page == "fix_assessment":
            st.switch_page("pages/fix_assessment.py")
        else:
            st.switch_page("pages/ict_assessment.py")

if __name__ == "__main__":
    main()
