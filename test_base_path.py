#!/usr/bin/env python3
"""
Script para verificar que base_path se está cargando correctamente
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("🔍 TEST: Verificando configuración de SHAREPOINT_BASE_PATH")
print("=" * 80)

# 1. Verificar .env
print("\n1️⃣ Variables en .env:")
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

sharepoint_base_path_env = os.getenv('SHAREPOINT_BASE_PATH', '')
print(f"   SHAREPOINT_BASE_PATH = '{sharepoint_base_path_env}'")

# 2. Verificar secrets.toml (si existe)
print("\n2️⃣ Verificando secrets.toml:")
secrets_path = Path(__file__).parent / ".streamlit" / "secrets.toml"
if secrets_path.exists():
    print(f"   ✅ Archivo existe: {secrets_path}")
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            try:
                base_path = st.secrets['sharepoint']['base_path']
                print(f"   📋 base_path en secrets: '{base_path}'")
            except:
                print("   ⚠️  No se pudo leer base_path de secrets")
        else:
            print("   ⚠️  st.secrets no disponible (normal si no corres con streamlit)")
    except ImportError:
        print("   ⚠️  streamlit no está instalado o no está corriendo")
else:
    print(f"   ❌ Archivo NO existe: {secrets_path}")

# 3. Cargar configuración con settings.py
print("\n3️⃣ Cargando configuración con Settings:")
try:
    from config import get_settings
    settings = get_settings()
    
    print(f"   Storage provider: {settings.storage.provider}")
    
    if settings.sharepoint:
        print(f"   ✅ SharePoint configurado:")
        print(f"      base_path: '{settings.sharepoint.base_path}'")
        print(f"      site_id: {settings.sharepoint.site_id[:30]}...")
        print(f"      drive_id: {settings.sharepoint.drive_id[:30]}...")
    else:
        print("   ❌ SharePoint NO configurado")
        
except Exception as e:
    print(f"   ❌ Error cargando settings: {e}")
    import traceback
    traceback.print_exc()

# 4. Verificar StorageService
print("\n4️⃣ Verificando StorageService:")
try:
    from services.storage_service import StorageService
    storage_service = StorageService()
    
    print(f"   Provider type: {type(storage_service.provider).__name__}")
    
    if hasattr(storage_service.provider, 'base_path'):
        print(f"   ✅ base_path en provider: '{storage_service.provider.base_path}'")
    else:
        print("   ❌ base_path NO disponible en provider")
        
    # Test: crear un path de prueba
    test_path = storage_service.provider.get_full_path("1_ICT", "MX", "Cliente", "Proyecto")
    print(f"   🧪 Path de prueba: '{test_path}'")
    
    if test_path.startswith("01_2025"):
        print("   ✅ ¡CORRECTO! El path inicia con 01_2025")
    else:
        print("   ❌ ¡ERROR! El path NO inicia con 01_2025")
        
except Exception as e:
    print(f"   ❌ Error creando StorageService: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("🎯 DIAGNÓSTICO:")
print("=" * 80)

if sharepoint_base_path_env:
    print(f"\n✅ SHAREPOINT_BASE_PATH está configurado en .env: '{sharepoint_base_path_env}'")
else:
    print("\n❌ SHAREPOINT_BASE_PATH NO está en .env o está vacío")

print("\n📋 Para corregir:")
print("   1. Verifica tu .env tenga: SHAREPOINT_BASE_PATH=\"01_2025\"")
print("   2. Si usas secrets.toml local, verifica: [sharepoint] base_path = \"01_2025\"")
print("   3. Reinicia la app: streamlit run main.py")
print("   4. Limpia cache: Menú ⋮ → Clear cache → Rerun")

print("\n" + "=" * 80)
