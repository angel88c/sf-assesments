#!/usr/bin/env python3
"""
Muestra la configuración completa necesaria para SharePoint en .env
"""

# Site response
site_response = {
    "id": "ibtest2020.sharepoint.com,0670681a-c391-4a3d-bc9b-e0f0b1b8dd09,d9c99339-198d-44e3-aae0-fc56e347e583",
    "name": "Public_Quotes_2025",
    "webUrl": "https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025"
}

# Drive response
drive_response = {
    "id": "b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9",
    "name": "Documentos"
}

print("=" * 70)
print("📋 CONFIGURACIÓN COMPLETA PARA .ENV")
print("=" * 70)

print("\n# ============================================================================")
print("# AZURE AD CONFIGURATION (ya tienes esto)")
print("# ============================================================================")
print("AZURE_TENANT_ID=58fc66f3-5586-4967-8302-03dc2a2f6513")
print("AZURE_CLIENT_ID=d779dfb6-8dfd-459d-9403-3a84b9f241eb")
print("AZURE_CLIENT_SECRET=lwD8Q~KinaJmvTuM.tWb9Tj1LhQE~tf2J2NXkbkU")

print("\n# ============================================================================")
print("# SHAREPOINT CONFIGURATION (agrega/actualiza esto)")
print("# ============================================================================")
print(f"SHAREPOINT_SITE_ID={site_response['id']}")
print(f"SHAREPOINT_DRIVE_ID={drive_response['id']}")

print("\n# Storage provider - cambiar cuando esté listo")
print("STORAGE_PROVIDER=local  # Cambiar a 'sharepoint' cuando funcione")

print("\n# ============================================================================")
print("# INFORMACIÓN ADICIONAL")
print("# ============================================================================")
print(f"# Site Name: {site_response['name']}")
print(f"# Site URL: {site_response['webUrl']}")
print(f"# Drive Name: {drive_response['name']}")

print("\n" + "=" * 70)
print("✅ Copia las líneas SHAREPOINT_* a tu archivo .env")
print("=" * 70)
