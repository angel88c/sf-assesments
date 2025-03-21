import os
import requests
import streamlit as st
from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"), override=True)

@st.cache_resource
def connect_to_salesforce():
    try:
        sf_info = dict()
        
        #Obtener credenciales desde el archivo .env
        sf_info["username"] = os.getenv('SALESFORCE_USERNAME')
        sf_info["password"] = os.getenv('SALESFORCE_PASSWORD')
        sf_info["security_token"] = os.getenv('SALESFORCE_SECURITY_TOKEN')
        sf_info["consumer_key"] = os.getenv('SALESFORCE_CONSUMER_KEY')
        sf_info["consumer_secret"] = os.getenv('SALESFORCE_CONSUMER_SECRET')
        #st.write(sf_info)
        
        # Conectar a Salesforce
        sf = Salesforce(
            username=sf_info["username"],
            password=sf_info["password"],
            security_token=sf_info["security_token"],
            consumer_key=sf_info["consumer_key"],
            consumer_secret=sf_info["consumer_secret"]
        )
        #st.success("Conexión exitosa a Salesforce!")
        
        redirect_uri = os.getenv("REDIRECT_URL")
        # f'https://login.salesforce.com/services/oauth2/token'
        token_url = os.getenv("TOKEN_URL")
        payload = {
            'grant_type': 'password',
            'client_id': sf_info["consumer_key"],
            'client_secret': sf_info["consumer_secret"],
            'username': sf_info["username"],
            'password': sf_info["password"] + sf_info["security_token"]
        }

        response = requests.post(token_url, data=payload)
        token_data = response.json()

        return sf

    except Exception as e:
        st.error(f"Error al conectar a Salesforce: {e}")
        return None
