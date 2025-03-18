import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"), override=True)

st.set_page_config(initial_sidebar_state="collapsed")

#Default app page
st.switch_page("pages/ict_assesment.py")
