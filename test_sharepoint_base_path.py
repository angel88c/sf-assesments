#!/usr/bin/env python3
"""
Test para verificar que SHAREPOINT_BASE_PATH funciona correctamente
sin duplicación
"""

import os
from dotenv import load_dotenv
from services.storage_service import StorageService
from pathlib import Path

load_dotenv()

def test_sharepoint_base_path():
    """Test de SharePoint base path sin duplicación."""
    
    print("=" * 80)
    print("🧪 TEST: SHAREPOINT_BASE_PATH SIN DUPLICACIÓN")
    print("=" * 80)
    
    # 1. Verificar configuración
    print("\n1️⃣ Configuración actual:")
    
    path_to_sharepoint = os.getenv("PATH_TO_SHAREPOINT")
    sharepoint_base_path = os.getenv("SHAREPOINT_BASE_PATH", "")
    storage_provider = os.getenv("STORAGE_PROVIDER", "local")
    
    print(f"   PATH_TO_SHAREPOINT = {path_to_sharepoint}")
    print(f"   SHAREPOINT_BASE_PATH = '{sharepoint_base_path}'")
    print(f"   STORAGE_PROVIDER = {storage_provider}")
    
    if storage_provider != "sharepoint":
        print("\n⚠️  STORAGE_PROVIDER no es 'sharepoint'")
        print("   Cambia a 'sharepoint' en .env para probar")
        return
    
    # 2. Inicializar StorageService
    print("\n2️⃣ Inicializando StorageService...")
    
    storage_service = StorageService()
    provider_name = type(storage_service.provider).__name__
    
    print(f"   ✅ Provider: {provider_name}")
    print(f"   ✅ Base path configurado: '{storage_service.provider.base_path}'")
    
    # 3. Simular creación de project path
    print("\n3️⃣ Simulando creación de project path...")
    
    test_data = {
        "projects_folder": "1_In_Circuit_Test_(ICT)",
        "country": "Mexico",
        "customer_name": "ACME_Corp",
        "project_name": "Test_Duplicacion_001"
    }
    
    # Simular get_full_path del provider
    from pages.utils.constants import COUNTRIES_DICT
    country_code = COUNTRIES_DICT.get(test_data["country"], "OTHER")
    
    project_path = storage_service.provider.get_full_path(
        test_data["projects_folder"],
        country_code,
        test_data["customer_name"],
        test_data["project_name"]
    )
    
    print(f"   Project path retornado: {project_path}")
    
    # 4. Verificar path
    print("\n4️⃣ Análisis del path:")
    
    path_parts = project_path.split("/")
    print(f"   Partes del path: {path_parts}")
    
    # Contar cuántas veces aparece base_path
    if sharepoint_base_path:
        count_base_path = project_path.count(sharepoint_base_path)
        print(f"\n   '{sharepoint_base_path}' aparece {count_base_path} vez/veces")
        
        if count_base_path > 1:
            print(f"   ❌ DUPLICACIÓN DETECTADA!")
            print(f"   Path: {project_path}")
        elif count_base_path == 1:
            print(f"   ✅ Correcto: '{sharepoint_base_path}' aparece solo una vez")
        else:
            print(f"   ⚠️  '{sharepoint_base_path}' NO aparece en el path")
    
    # 5. Generar URL de Salesforce
    print("\n5️⃣ Generando URL para Salesforce...")
    
    # Simular _get_sharepoint_url
    base_url = path_to_sharepoint
    project_relative = str(Path(project_path)).replace("\\", "/").lstrip("/")
    
    if base_url.endswith("/"):
        sharepoint_url = f"{base_url}{project_relative}"
    else:
        sharepoint_url = f"{base_url}/{project_relative}"
    
    print(f"   URL generada:")
    print(f"   {sharepoint_url}")
    
    # 6. Verificar URL
    print("\n6️⃣ Verificación de URL:")
    
    if sharepoint_base_path:
        url_count = sharepoint_url.count(sharepoint_base_path)
        print(f"   '{sharepoint_base_path}' aparece {url_count} vez/veces en la URL")
        
        if url_count > 1:
            print(f"   ❌ DUPLICACIÓN en URL")
        elif url_count == 1:
            print(f"   ✅ Correcto: sin duplicación")
        else:
            print(f"   ⚠️  '{sharepoint_base_path}' no aparece en URL")
    
    # 7. Resultado final
    print("\n" + "=" * 80)
    print("📊 RESULTADO FINAL")
    print("=" * 80)
    
    print(f"\n📁 Carpeta en SharePoint:")
    print(f"   {project_path}")
    
    print(f"\n🔗 URL en Salesforce:")
    print(f"   {sharepoint_url}")
    
    if sharepoint_base_path:
        # Estructura esperada
        expected_parts = [sharepoint_base_path, test_data["projects_folder"], country_code, 
                         test_data["customer_name"], test_data["project_name"]]
        expected_path = "/".join(expected_parts)
        
        print(f"\n✅ Estructura esperada:")
        print(f"   {expected_path}")
        
        if project_path == expected_path:
            print(f"\n🎉 ¡PERFECTO! Path coincide con lo esperado")
        else:
            print(f"\n⚠️  Path difiere de lo esperado")
            print(f"   Esperado: {expected_path}")
            print(f"   Actual:   {project_path}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        test_sharepoint_base_path()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
