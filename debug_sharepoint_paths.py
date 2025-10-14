#!/usr/bin/env python3
"""
Debug de rutas de SharePoint
Ayuda a identificar el problema de duplicación de 01_2025
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 DEBUG: RUTAS DE SHAREPOINT")
print("=" * 80)

# Variables de entorno
path_to_sharepoint = os.getenv("PATH_TO_SHAREPOINT", "")
sharepoint_base_path = os.getenv("SHAREPOINT_BASE_PATH", "")
path_file = os.getenv("PATH_FILE", "")

print(f"\n📋 Variables en .env:")
print(f"   PATH_TO_SHAREPOINT = {path_to_sharepoint}")
print(f"   SHAREPOINT_BASE_PATH = '{sharepoint_base_path}'")
print(f"   PATH_FILE = {path_file}")

print("\n" + "=" * 80)
print("🔍 ANÁLISIS")
print("=" * 80)

# Verificar si PATH_TO_SHAREPOINT ya incluye 01_2025
if "01_2025" in path_to_sharepoint.lower():
    print("\n⚠️  PROBLEMA DETECTADO:")
    print(f"   PATH_TO_SHAREPOINT ya incluye '01_2025':")
    print(f"   {path_to_sharepoint}")
    print(f"\n   Si además SHAREPOINT_BASE_PATH='01_2025':")
    print(f"   Se duplica: {path_to_sharepoint}/01_2025")
    print("\n   ❌ Resultado: 01_2025/01_2025/1_ICT/...")
else:
    print("\n✅ PATH_TO_SHAREPOINT NO incluye '01_2025'")
    print(f"   {path_to_sharepoint}")

print("\n" + "=" * 80)
print("💡 SOLUCIONES")
print("=" * 80)

print("\n🎯 OPCIÓN 1: URL de Salesforce incluye 01_2025")
print("   PATH_TO_SHAREPOINT = https://.../Documentos/01_2025")
print("   SHAREPOINT_BASE_PATH = (vacío)")
print("\n   Resultado en SharePoint: 01_2025/1_ICT/MX/...")
print("   Resultado URL Salesforce: https://.../Documentos/01_2025/1_ICT/...")

print("\n🎯 OPCIÓN 2: URL de Salesforce NO incluye 01_2025")
print("   PATH_TO_SHAREPOINT = https://.../Documentos")
print("   SHAREPOINT_BASE_PATH = 01_2025")
print("\n   Resultado en SharePoint: 01_2025/1_ICT/MX/...")
print("   Resultado URL Salesforce: https://.../Documentos/01_2025/1_ICT/...")

print("\n" + "=" * 80)
print("✅ RECOMENDACIÓN")
print("=" * 80)

if "01_2025" in path_to_sharepoint.lower():
    print("\n🔧 Tu PATH_TO_SHAREPOINT ya incluye '01_2025'")
    print("\n   ✅ SOLUCIÓN: Deja SHAREPOINT_BASE_PATH vacío")
    print("\n   En tu .env:")
    print(f"   PATH_TO_SHAREPOINT={path_to_sharepoint}")
    print("   SHAREPOINT_BASE_PATH=")
    print("\n   Las carpetas se crearán en: 01_2025/1_ICT/MX/...")
    print("   (porque SHAREPOINT_BASE_PATH extrae '01_2025' de PATH_TO_SHAREPOINT)")
else:
    print("\n🔧 Tu PATH_TO_SHAREPOINT NO incluye '01_2025'")
    print("\n   ✅ SOLUCIÓN: Configura SHAREPOINT_BASE_PATH=01_2025")
    print("\n   En tu .env:")
    print(f"   PATH_TO_SHAREPOINT={path_to_sharepoint}")
    print("   SHAREPOINT_BASE_PATH=01_2025")

print("\n" + "=" * 80)
