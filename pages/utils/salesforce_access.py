"""
Salesforce Access Module

This module provides functions for connecting to Salesforce and retrieving data.
It handles authentication, connection, and data retrieval operations.
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv
from simple_salesforce import Salesforce

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"), override=True)

@st.cache_resource
def connect_to_salesforce():
    """
    Connect to Salesforce using credentials from environment variables.
    
    Returns:
        Salesforce: Authenticated Salesforce instance or None if connection fails
    """
    try:
        # Get credentials from environment variables
        sf_credentials = {
            "username": os.getenv('SALESFORCE_USERNAME'),
            "password": os.getenv('SALESFORCE_PASSWORD'),
            "security_token": os.getenv('SALESFORCE_SECURITY_TOKEN'),
            "consumer_key": os.getenv('SALESFORCE_CONSUMER_KEY'),
            "consumer_secret": os.getenv('SALESFORCE_CONSUMER_SECRET')
        }
        
        # Connect to Salesforce
        sf = Salesforce(
            username=sf_credentials["username"],
            password=sf_credentials["password"],
            security_token=sf_credentials["security_token"],
            consumer_key=sf_credentials["consumer_key"],
            consumer_secret=sf_credentials["consumer_secret"]
        )
        
        # Get OAuth token
        token_url = os.getenv("TOKEN_URL")
        payload = {
            'grant_type': 'password',
            'client_id': sf_credentials["consumer_key"],
            'client_secret': sf_credentials["consumer_secret"],
            'username': sf_credentials["username"],
            'password': sf_credentials["password"] + sf_credentials["security_token"]
        }

        response = requests.post(token_url, data=payload)
        token_data = response.json()

        return sf

    except Exception as e:
        st.error(f"Error connecting to Salesforce: {e}")
        return None

@st.cache_resource
def get_unique_account_dict():
    """
    Get a dictionary of unique Salesforce accounts.
    
    Returns:
        dict: Dictionary mapping account IDs to account names
    """
    sf = st.session_state.salesforce
    
    if sf is None:
        return {}
    
    accounts_dict = {}
    seen_names = set()
    
    try:
        # Query Salesforce for accounts
        query = "SELECT Id, Name from Account order by Name ASC"
        result = sf.query(query)
        
        # Process results
        for record in result["records"]:
            name = record["Name"]
            
            if name not in seen_names:
                accounts_dict[record["Id"]] = name
                seen_names.add(name)
        
        # Add "Other" option if not present
        if "Other" not in seen_names:
            accounts_dict["other"] = "Other"
            
        return accounts_dict
        
    except Exception as e:
        st.error(f'Error querying Salesforce accounts: {e}')
        return {"other": "Other"}