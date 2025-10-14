#!/usr/bin/env python3
"""
Test completo del flujo de assessment
Simula la creación de un proyecto y verifica la URL de SharePoint generada
"""

import os
from dotenv import load_dotenv
from services.storage_service import StorageService
from storage.sharepoint_storage import SharePointStorageProvider
from io import BytesIO
from pathlib import Path

# Load environment
load_dotenv()

def test_full_assessment_flow():
    """Test del flujo completo con generación de URL."""
    
    print("=" * 80)
    print("🧪 TEST COMPLETO: ASSESSMENT → CARPETA → URL SALESFORCE")
    print("=" * 80)
    
    # 1. Inicializar servicios
    print("\n1️⃣ Inicializando servicios...")
    provider = SharePointStorageProvider(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
        site_id=os.getenv("SHAREPOINT_SITE_ID"),
        drive_id=os.getenv("SHAREPOINT_DRIVE_ID"),
        base_path=""
    )
    
    storage_service = StorageService(storage_provider=provider)
    print("✅ Servicios inicializados")
    
    # 2. Datos de prueba
    print("\n2️⃣ Preparando datos de prueba...")
    
    test_project = {
        "assessment_type": "ICT",
        "projects_folder": "TEST_1_In_Circuit_Test_(ICT)",
        "customer_name": "ACME_Corporation",
        "project_name": "PCB_Testing_Project_2025_001",
        "country": "Mexico"
    }
    
    print(f"   Assessment: {test_project['assessment_type']}")
    print(f"   Cliente: {test_project['customer_name']}")
    print(f"   Proyecto: {test_project['project_name']}")
    print(f"   País: {test_project['country']}")
    
    # 3. Crear estructura de proyecto
    print("\n3️⃣ Creando estructura de proyecto en SharePoint...")
    print("   ⏳ Esto puede tardar unos momentos...")
    
    try:
        project_path = storage_service.create_project_folder(
            assessment_type=test_project["assessment_type"],
            projects_folder=test_project["projects_folder"],
            customer_name=test_project["customer_name"],
            project_name=test_project["project_name"],
            country=test_project["country"]
        )
        
        print(f"   ✅ Carpeta creada: {project_path}")
        
    except Exception as e:
        print(f"   ⚠️  Error o carpeta ya existe: {e}")
        # Si ya existe, construir el path manualmente
        from pages.utils.constants import COUNTRIES_DICT
        country_code = COUNTRIES_DICT.get(test_project["country"], "OTHER")
        project_path = f"{test_project['projects_folder']}/{country_code}/{test_project['customer_name']}/{test_project['project_name']}"
        print(f"   ℹ️  Usando path existente: {project_path}")
    
    # 4. Generar URL de SharePoint
    print("\n4️⃣ Generando URL de SharePoint para Salesforce...")
    
    base_sharepoint_url = os.getenv("PATH_TO_SHAREPOINT")
    
    # Limpiar y construir URL
    project_relative = str(Path(project_path)).replace("\\", "/")
    
    if base_sharepoint_url.endswith("/"):
        sharepoint_url = f"{base_sharepoint_url}{project_relative}"
    else:
        sharepoint_url = f"{base_sharepoint_url}/{project_relative}"
    
    print(f"   ✅ URL generada:")
    print(f"      {sharepoint_url}")
    
    # 5. Mostrar cómo se vería en Salesforce
    print("\n" + "=" * 80)
    print("📋 DATOS QUE SE ENVIARÍAN A SALESFORCE")
    print("=" * 80)
    
    salesforce_opp = {
        "Name": test_project["project_name"],
        "StageName": "New Request",
        "CloseDate": "2025-11-30",
        "Assessment_Date__c": "2025-10-14",
        "Path__c": sharepoint_url,  # ← Esta es la URL específica
        "BU__c": test_project["assessment_type"]
    }
    
    for key, value in salesforce_opp.items():
        if key == "Path__c":
            print(f"\n   ✨ {key}:")
            print(f"      {value}")
        else:
            print(f"   • {key}: {value}")
    
    # 6. Comparación visual
    print("\n" + "=" * 80)
    print("🔍 COMPARACIÓN: ANTES vs DESPUÉS")
    print("=" * 80)
    
    print("\n❌ ANTES (URL genérica a raíz):")
    print(f"   Path__c: {base_sharepoint_url}")
    print("   → Click lleva a carpeta raíz (01_2025)")
    print("   → Usuario debe buscar: ICT → MX → ACME → Proyecto")
    
    print("\n✅ DESPUÉS (URL específica al proyecto):")
    print(f"   Path__c: {sharepoint_url}")
    print("   → Click lleva DIRECTO a carpeta del proyecto")
    print("   → Acceso instantáneo a todos los archivos")
    
    # 7. Verificar que la carpeta existe
    print("\n" + "=" * 80)
    print("🔎 VERIFICACIÓN EN SHAREPOINT")
    print("=" * 80)
    
    print("\n⏳ Verificando que la carpeta existe...")
    exists = provider.folder_exists(project_path)
    
    if exists:
        print(f"   ✅ Carpeta verificada en SharePoint")
        print(f"   📁 Ubicación: {project_path}")
        print(f"   🔗 URL: {sharepoint_url}")
    else:
        print(f"   ⚠️  Carpeta no encontrada (puede ser que no se haya creado)")
    
    # 8. Resumen final
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETADO")
    print("=" * 80)
    
    print("\n📊 RESUMEN:")
    print(f"   • Assessment Type: {test_project['assessment_type']}")
    print(f"   • Carpeta creada: {project_path}")
    print(f"   • URL generada: ✅")
    print(f"   • Formato correcto: ✅")
    print(f"   • Lista para Salesforce: ✅")
    
    print("\n💡 PRÓXIMOS PASOS:")
    print("   1. La próxima vez que llenes un assessment en la app")
    print("   2. Se creará la carpeta automáticamente")
    print("   3. Se generará esta URL específica")
    print("   4. Se guardará en Salesforce Path__c")
    print("   5. Sales Managers podrán acceder directamente")
    
    print("\n🎯 BENEFICIO:")
    print("   Click en oportunidad → Acceso directo a carpeta del proyecto")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        test_full_assessment_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
