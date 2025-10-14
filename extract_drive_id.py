#!/usr/bin/env python3
"""
Extrae el Drive ID correcto del response de SharePoint
"""

# Response del test anterior
response_json = {
    '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#drives',
    'value': [{
        'createdDateTime': '2024-12-15T06:54:49Z',
        'description': '',
        'id': 'b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9',
        'lastModifiedDateTime': '2025-07-02T20:07:41Z',
        'name': 'Documentos',
        'webUrl': 'https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos%20compartidos',
        'driveType': 'documentLibrary',
    }]
}

# Extraer Drive ID
drive_id = response_json['value'][0]['id']
drive_name = response_json['value'][0]['name']

print("=" * 70)
print("DRIVE ID CORRECTO PARA TU .ENV")
print("=" * 70)
print(f"\nDrive Name: {drive_name}")
print(f"Drive ID: {drive_id}")
print("\n📝 Agrega esto a tu .env:")
print(f"\nSHAREPOINT_DRIVE_ID={drive_id}")
print("\n" + "=" * 70)
