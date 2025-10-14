# test_sharepoint_access.py
from msal import ConfidentialClientApplication
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .ENV file
load_dotenv(".env")

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")

# Obtener token
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" in result:
    print("✅ Token obtenido exitosamente")
    
    # Probar acceso a SharePoint
    headers = {"Authorization": f"Bearer {result['access_token']}"}
    
    # Listar drives
    site_id = os.getenv("SHAREPOINT_SITE_ID")
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Acceso a SharePoint exitoso")
        print(f"Drives encontrados: {len(response.json()['value'])}")
        print(response.json())
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
else:
    print(f"❌ Error obteniendo token: {result.get('error_description')}")