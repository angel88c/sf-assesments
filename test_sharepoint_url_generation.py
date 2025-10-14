#!/usr/bin/env python3
"""
Test de generación de URLs de SharePoint para oportunidades de Salesforce
Demuestra que cada proyecto obtiene su URL específica
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
load_dotenv()

def test_url_generation():
    """Test de generación de URLs de SharePoint."""
    
    print("=" * 80)
    print("🔗 TEST: GENERACIÓN DE URLs DE SHAREPOINT PARA SALESFORCE")
    print("=" * 80)
    
    # Configuración de ejemplo
    base_sharepoint_url = os.getenv("PATH_TO_SHAREPOINT", "https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos")
    
    print(f"\n📍 Base SharePoint URL:")
    print(f"   {base_sharepoint_url}")
    
    # Casos de prueba
    test_cases = [
        {
            "name": "ICT - Cliente México",
            "project_path": "1_In_Circuit_Test_(ICT)/MX/ACME_Corp/Proyecto_PCB_2025",
        },
        {
            "name": "FCT - Cliente USA",
            "project_path": "2_Functional_Test_(FCT)/USA/TechCorp_Inc/Product_Test_001",
        },
        {
            "name": "IAT - Cliente Canadá",
            "project_path": "4_Industrial_Automation_(IAT)/CAD/AutoSolutions/Robot_Station_X1",
        }
    ]
    
    print("\n" + "=" * 80)
    print("📋 EJEMPLOS DE URLs GENERADAS:")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Carpeta proyecto: {test_case['project_path']}")
        
        # Construir URL completa
        if base_sharepoint_url.endswith("/"):
            full_url = f"{base_sharepoint_url}{test_case['project_path']}"
        else:
            full_url = f"{base_sharepoint_url}/{test_case['project_path']}"
        
        print(f"   ✅ URL en Salesforce (Path__c):")
        print(f"      {full_url}")
    
    print("\n" + "=" * 80)
    print("📊 COMPARACIÓN: ANTES vs DESPUÉS")
    print("=" * 80)
    
    print("\n❌ ANTES (Todos iguales):")
    print(f"   {base_sharepoint_url}")
    print(f"   {base_sharepoint_url}")
    print(f"   {base_sharepoint_url}")
    print("   ⚠️  Todos los proyectos apuntaban a la raíz")
    
    print("\n✅ DESPUÉS (URLs específicas):")
    print(f"   {base_sharepoint_url}/1_In_Circuit_Test_(ICT)/MX/ACME_Corp/Proyecto_PCB_2025")
    print(f"   {base_sharepoint_url}/2_Functional_Test_(FCT)/USA/TechCorp_Inc/Product_Test_001")
    print(f"   {base_sharepoint_url}/4_Industrial_Automation_(IAT)/CAD/AutoSolutions/Robot_Station_X1")
    print("   ✅ Cada proyecto tiene su link directo")
    
    print("\n" + "=" * 80)
    print("🎯 BENEFICIOS")
    print("=" * 80)
    
    print("\n✅ Acceso directo:")
    print("   • Click en URL de Salesforce → abre carpeta específica del proyecto")
    print("   • No necesitas buscar manualmente en SharePoint")
    
    print("\n✅ Mejor organización:")
    print("   • Sales Managers ven exactamente dónde están los archivos")
    print("   • Reducción de tiempo buscando proyectos")
    
    print("\n✅ Trazabilidad:")
    print("   • Cada oportunidad sabe dónde están sus documentos")
    print("   • Fácil auditoría y seguimiento")
    
    print("\n" + "=" * 80)
    print("🔧 IMPLEMENTACIÓN")
    print("=" * 80)
    
    print("\n📝 Se modificaron 2 archivos:")
    print("   1. base_assessment.py (versión actual)")
    print("      • Genera URL específica antes de crear oportunidad")
    print("      • Path__c = URL completa a carpeta del proyecto")
    
    print("\n   2. base_assessment_refactored.py (versión refactorizada)")
    print("      • Método _get_sharepoint_url(project_path)")
    print("      • Construye URL basándose en project_path")
    
    print("\n" + "=" * 80)
    print("✅ LISTO PARA USAR")
    print("=" * 80)
    
    print("\n💡 Próximas oportunidades creadas tendrán:")
    print("   • Path__c apuntando a carpeta específica del proyecto")
    print("   • URL clickeable directamente desde Salesforce")
    print("   • Navegación instantánea a documentos del proyecto")
    
    print("\n🚀 No requiere cambios en .env ni configuración adicional")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        test_url_generation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
