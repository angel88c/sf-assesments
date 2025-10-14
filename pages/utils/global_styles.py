"""
Global Styles Module

This module provides functions for setting global styles and loading the iBtest logo.
"""

import streamlit as st
from PIL import Image

def set_global_styles():
    """
    Set global CSS styles for the application.
    """
    st.markdown("""
        <style>           
            /* Page background */
            body {
                background-color: #f0faf9 !important;
            }

            /* Main container background */
            [data-testid="stAppViewContainer"] {
                background-color: #f0faf9 !important;
            }

            /* Form styling */
            div[data-testid="stForm"] {
                background-color: white !important;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
            
            /* Button styling */
            div[data-testid="stForm"] button {
                background-color: #16337d !important;
                color: white !important;
                border-radius: 5px;
                border: 2px solid #16337d;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                height: 30px;
            }

            /* Button hover effect */
            div[data-testid="stForm"] button:hover {
                background-color: #00072d !important;
                border-color: #00072d;
            }
        </style>
    """, unsafe_allow_html=True)

def load_ibtest_logo():
    """
    Load and display the iBtest logo.
    """
    try:
        logo = Image.open("logo_ibtest.png")
        st.image(logo, width=150)
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        st.write("iBtest")


def subtitle_h2(text: str):
    st.markdown(f"<h2>{text}</h2>", unsafe_allow_html=True)
    
def subtitle_h3(text: str):
    st.markdown(f"<h3>{text}</h3>", unsafe_allow_html=True)

def subtitle_h4(text: str):
    st.markdown(f"<h4>{text}</h4>", unsafe_allow_html=True)
    
    