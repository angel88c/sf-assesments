#!/usr/bin/env python3
"""
Test completo de SharePoint Storage Provider
Prueba: crear carpetas, copiar templates, subir archivos
"""

import os
from dotenv import load_dotenv
from storage.sharepoint_storage import SharePointStorageProvider
from pathlib import Path
from io import BytesIO

# Load environment
load_dotenv()

def test_sharepoint_complete():
    """Test completo de operaciones en SharePoint."""
    
    print("=" * 70)
    print("PRUEBA COMPLETA DE SHAREPOINT STORAGE")
    print("=" * 70)
    
    # 1. Crear provider
    print("\n1️⃣ Inicializando SharePoint Provider...")
    provider = SharePointStorageProvider(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
        site_id=os.getenv("SHAREPOINT_SITE_ID"),
        drive_id=os.getenv("SHAREPOINT_DRIVE_ID"),
        base_path="test_projects"  # Carpeta raíz para pruebas
    )
    print("✅ Provider inicializado")
    
    # 2. Crear carpeta de prueba
    print("\n2️⃣ Creando carpeta de prueba...")
    test_folder = "TEST_ICT_2025/ACME_Corp/Proyecto_Prueba_001"
    try:
        provider.create_folder(test_folder)
        print(f"✅ Carpeta creada: {test_folder}")
    except Exception as e:
        print(f"⚠️  Error (puede ya existir): {e}")
    
    # 3. Subir archivo de prueba
    print("\n3️⃣ Subiendo archivo de prueba...")
    test_content = "Este es un archivo de prueba\nCreado desde Python\n"
    file_content = BytesIO(test_content.encode('utf-8'))
    
    try:
        provider.upload_file(file_content, test_folder, "test_file.txt")
        print(f"✅ Archivo subido: test_file.txt")
    except Exception as e:
        print(f"❌ Error subiendo archivo: {e}")
    
    # 4. Copiar template (solo si tienes uno local)
    template_path = os.getenv("TEMPLATE_ICT")
    if template_path and Path(template_path).exists():
        print(f"\n4️⃣ Copiando template desde: {template_path}")
        print("⚠️  Esto puede tardar varios segundos/minutos dependiendo del tamaño...")
        
        try:
            destination = f"TEST_ICT_2025/ACME_Corp/Proyecto_Con_Template"
            provider.copy_template(template_path, destination)
            print(f"✅ Template copiado exitosamente")
        except Exception as e:
            print(f"❌ Error copiando template: {e}")
    else:
        print(f"\n4️⃣ ⏭️  Saltando prueba de template (TEMPLATE_ICT no configurado o no existe)")
    
    # 5. Verificar que carpeta existe
    print("\n5️⃣ Verificando existencia de carpeta...")
    exists = provider.folder_exists(test_folder)
    print(f"✅ Carpeta existe: {exists}")
    
    print("\n" + "=" * 70)
    print("✅ PRUEBA COMPLETA FINALIZADA")
    print("=" * 70)
    print("\n📁 Revisa tu SharePoint en:")
    print(f"   test_projects/{test_folder}")
    print("\n💡 Si todo funcionó, puedes cambiar STORAGE_PROVIDER=sharepoint en .env")


if __name__ == "__main__":
    try:
        test_sharepoint_complete()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por usuario")
    except Exception as e:
        print(f"\n❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()
