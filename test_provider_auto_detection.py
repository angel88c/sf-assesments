#!/usr/bin/env python3
"""
Test de auto-detección del Storage Provider
Verifica que el sistema use el provider correcto según STORAGE_PROVIDER en .env
"""

import os
from dotenv import load_dotenv
from services.storage_service import StorageService
from config import get_settings

# Load environment
load_dotenv()

def test_provider_detection():
    """Test que verifica la auto-detección del provider."""
    
    print("=" * 80)
    print("🔍 TEST: AUTO-DETECCIÓN DE STORAGE PROVIDER")
    print("=" * 80)
    
    # 1. Verificar configuración
    print("\n1️⃣ Verificando configuración en .env...")
    
    storage_provider_env = os.getenv("STORAGE_PROVIDER", "local")
    print(f"   STORAGE_PROVIDER = {storage_provider_env}")
    
    # 2. Cargar settings
    print("\n2️⃣ Cargando configuración...")
    settings = get_settings()
    
    print(f"   ✅ Storage provider configurado: {settings.storage.provider}")
    
    if settings.storage.provider == 'sharepoint':
        print(f"   ✅ Azure configurado:")
        print(f"      • Tenant ID: {settings.azure.tenant_id[:20]}...")
        print(f"      • Client ID: {settings.azure.client_id[:20]}...")
        print(f"   ✅ SharePoint configurado:")
        print(f"      • Site ID: {settings.sharepoint.site_id[:40]}...")
        print(f"      • Drive ID: {settings.sharepoint.drive_id[:40]}...")
    
    # 3. Inicializar StorageService
    print("\n3️⃣ Inicializando StorageService (auto-detecta provider)...")
    
    storage_service = StorageService()
    
    provider_name = type(storage_service.provider).__name__
    print(f"   ✅ Provider detectado: {provider_name}")
    
    # 4. Resultado
    print("\n" + "=" * 80)
    print("📊 RESULTADO")
    print("=" * 80)
    
    if storage_provider_env.lower() == 'sharepoint':
        if provider_name == 'SharePointStorageProvider':
            print("\n✅ ¡CORRECTO!")
            print("   • STORAGE_PROVIDER=sharepoint en .env")
            print("   • StorageService usa SharePointStorageProvider")
            print("   • Las carpetas se crearán en SharePoint")
            print("   • Los templates se copiarán a SharePoint")
        else:
            print("\n❌ ERROR")
            print("   • STORAGE_PROVIDER=sharepoint en .env")
            print(f"   • Pero StorageService usa {provider_name}")
            print("   • Algo está mal configurado")
    else:
        if provider_name == 'LocalStorageProvider':
            print("\n✅ CORRECTO")
            print("   • STORAGE_PROVIDER=local (o no configurado)")
            print("   • StorageService usa LocalStorageProvider")
            print("   • Las carpetas se crearán localmente")
        else:
            print("\n⚠️  INESPERADO")
            print(f"   • Provider detectado: {provider_name}")
    
    # 5. Instrucciones
    print("\n" + "=" * 80)
    print("🔧 PARA CAMBIAR A SHAREPOINT")
    print("=" * 80)
    
    if storage_provider_env.lower() != 'sharepoint':
        print("\n1. Abre tu archivo .env")
        print("\n2. Cambia o agrega:")
        print("   STORAGE_PROVIDER=sharepoint")
        print("\n3. Asegúrate de tener configurado:")
        print("   • AZURE_TENANT_ID")
        print("   • AZURE_CLIENT_ID")
        print("   • AZURE_CLIENT_SECRET")
        print("   • SHAREPOINT_SITE_ID")
        print("   • SHAREPOINT_DRIVE_ID")
        print("\n4. Reinicia la aplicación")
    else:
        print("\n✅ Ya está configurado para SharePoint")
        print("   Reinicia la aplicación si hiciste cambios recientes")
    
    print("\n" + "=" * 80)
    
    return provider_name


if __name__ == "__main__":
    try:
        provider = test_provider_detection()
        
        print("\n💡 VERIFICACIÓN FINAL:")
        if provider == "SharePointStorageProvider":
            print("   ✅ La próxima vez que crees un assessment,")
            print("      la carpeta SE CREARÁ EN SHAREPOINT")
        else:
            print("   ℹ️  Actualmente usando almacenamiento local")
            print("      Cambia STORAGE_PROVIDER=sharepoint para usar SharePoint")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
