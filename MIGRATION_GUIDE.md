# Guía de Migración - Arquitectura Refactorizada

Esta guía explica cómo migrar gradualmente a la nueva arquitectura sin interrumpir la funcionalidad actual.

## 📋 Tabla de Contenidos

1. [Resumen de Cambios](#resumen-de-cambios)
2. [Estrategia de Migración](#estrategia-de-migración)
3. [Paso a Paso](#paso-a-paso)
4. [Actualizar Variables de Entorno](#actualizar-variables-de-entorno)
5. [Testing](#testing)
6. [Rollback](#rollback)

---

## Resumen de Cambios

### Nuevos Módulos Creados

```
✅ config/
   ├── __init__.py
   └── settings.py              # Configuración centralizada

✅ core/
   ├── __init__.py
   ├── auth.py                  # Servicio de autenticación
   ├── exceptions.py            # Excepciones personalizadas
   └── logging_config.py        # Configuración de logging

✅ services/
   ├── __init__.py
   ├── salesforce_service.py    # Servicio de Salesforce
   └── storage_service.py       # Servicio de almacenamiento

✅ storage/
   ├── __init__.py
   ├── base.py                  # Interface de almacenamiento
   ├── local_storage.py         # Implementación local (actual)
   └── sharepoint_storage.py    # Implementación SharePoint (futuro)

✅ pages/utils/
   └── base_assessment_refactored.py  # BaseAssessment mejorado
```

### Archivos Modificados

```
📝 main.py                      # Usa AuthService
📝 requirements.txt             # (puede requerir msal para SharePoint)
```

---

## Estrategia de Migración

### Opción 1: Migración Gradual (Recomendada)

Ambas versiones coexisten. Puedes probar la nueva arquitectura sin afectar la producción.

**Ventajas:**
- Sin riesgo de romper funcionalidad existente
- Tiempo para testing exhaustivo
- Rollback instantáneo si hay problemas

**Desventajas:**
- Código duplicado temporalmente
- Requiere mantenimiento paralelo

### Opción 2: Migración Completa

Reemplazar completamente todos los módulos.

**Ventajas:**
- Código limpio sin duplicados
- Aprovecha todos los beneficios inmediatamente

**Desventajas:**
- Mayor riesgo
- Requiere testing completo antes de deploy

---

## Paso a Paso

### Fase 1: Preparación (Ya completado ✅)

1. **Crear nuevos módulos** (✅ Hecho)
2. **Actualizar main.py** (✅ Hecho)
3. **Crear documentación** (✅ En progreso)

### Fase 2: Actualizar Variables de Entorno

Asegúrate de que tu `.env` tenga todas las variables necesarias:

```bash
# Salesforce
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token
SALESFORCE_CONSUMER_KEY=your_key
SALESFORCE_CONSUMER_SECRET=your_secret
TOKEN_URL=https://login.salesforce.com/services/oauth2/token
SF_TIMEOUT=30

# Storage
PATH_FILE=/path/to/your/files
PATH_TO_SHAREPOINT=/path/to/sharepoint
TEMPLATE_ICT=/path/to/ict/template
TEMPLATE_FCT=/path/to/fct/template
TEMPLATE_IAT=/path/to/iat/template

# Authentication
APP_PASSWORD=your_hashed_password
```

**Verificar configuración:**

```python
python -c "from config import get_settings; settings = get_settings(); print('✅ Config loaded successfully')"
```

### Fase 3: Migrar Assessment Pages (Uno a la vez)

#### Ejemplo: Migrar ICT Assessment

**Opción A: Crear nueva versión (Seguro)**

1. Crear `pages/ict_assessment_v2.py`:

```python
"""
ICT Assessment Module (Refactored)
"""

import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

from pages.utils.base_assessment_refactored import BaseAssessment
from pages.utils.ict_create_html import json_to_html
from pages.utils.constants import (
    YES_NO, REQ_OPTIONS, ACTIVATION_TYPES, 
    WELL_TYPES, SIZE_TYPES, OPTIONS
)
from pages.utils.global_styles import subtitle_h2, subtitle_h3, subtitle_h4
from core.auth import require_authentication

# Protect page with authentication decorator
@require_authentication
def main():
    """Main function to run the ICT assessment."""
    # Same ICT_FILE_TYPES and create_ict_specific_sections as before
    
    ICT_FILE_TYPES = {
        '*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)': False,
        '*BOM': False,
        'Gerber files': False,
        'Schematics (pdf)': False,
        'Test Spec (pdf, doc)': False,
        'Fixture SOW': False,
        'Board directory (.tar.gz, .tar)': False,
    }
    
    def create_ict_specific_sections(info):
        # Same implementation as current ict_assessment.py
        pass
    
    # Create ICT assessment instance with refactored base
    ict_assessment = BaseAssessment(
        assessment_type="ICT",
        title="In Circuit Test Assessment",
        projects_folder="1_In_Circuit Test (ICT)"
    )
    
    # Render the form
    ict_assessment.render_form(
        file_types=ICT_FILE_TYPES,
        html_converter=json_to_html,
        additional_sections=create_ict_specific_sections
    )

if __name__ == "__main__":
    main()
```

2. Probar `ict_assessment_v2.py` exhaustivamente
3. Si funciona, renombrar:
   ```bash
   mv pages/ict_assessment.py pages/ict_assessment_old.py
   mv pages/ict_assessment_v2.py pages/ict_assessment.py
   ```

**Opción B: Modificar directamente (Más rápido)**

1. En `pages/ict_assessment.py`, cambiar import:

```python
# ANTES
from pages.utils.base_assessment import BaseAssessment

# DESPUÉS
from pages.utils.base_assessment_refactored import BaseAssessment
```

2. Agregar decorador de autenticación:

```python
from core.auth import require_authentication

@require_authentication
def main():
    # ... resto del código
```

3. Remover validación manual de autenticación:

```python
# ELIMINAR ESTO:
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access this page")
    st.switch_page("main.py")
```

### Fase 4: Testing

#### Test Manual

1. **Login:**
   ```bash
   streamlit run main.py
   ```
   - Verificar que login funciona
   - Verificar redirección correcta

2. **Assessment Form:**
   - Llenar formulario completo
   - Upload archivos
   - Submit

3. **Verificar:**
   - ✅ Carpeta creada correctamente
   - ✅ Archivos subidos
   - ✅ HTML generado
   - ✅ Oportunidad en Salesforce

#### Test Automatizado (Opcional pero recomendado)

Crear `tests/test_services.py`:

```python
import pytest
from services.storage_service import StorageService
from storage.local_storage import LocalStorageProvider
from pathlib import Path

def test_storage_service():
    """Test storage service basic operations."""
    provider = LocalStorageProvider(Path("/tmp/test"))
    service = StorageService(provider)
    
    # Test should pass
    assert service is not None

def test_config_loading():
    """Test configuration loading."""
    from config import get_settings
    settings = get_settings()
    assert settings.salesforce.username is not None
```

Ejecutar tests:
```bash
pytest tests/
```

### Fase 5: Repetir para FCT y IAT

Una vez que ICT funcione correctamente, repetir el proceso para:
- `pages/fct_assessment.py`
- `pages/iat_assessment.py`

---

## Actualizar Variables de Entorno

### Crear `.env.example`

Para nuevos desarrolladores, crear template:

```bash
cp .env .env.example
# Editar .env.example y reemplazar valores reales con placeholders
```

### Validar Configuración

Script para validar que todas las variables estén configuradas:

```python
# scripts/validate_config.py
from config.settings import Settings

try:
    settings = Settings.load_from_env()
    print("✅ All configuration loaded successfully!")
    print(f"   - Salesforce user: {settings.salesforce.username}")
    print(f"   - Storage path: {settings.storage.base_path}")
    print(f"   - Templates configured: ICT, FCT, IAT")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("   Please check your .env file")
```

Ejecutar:
```bash
python scripts/validate_config.py
```

---

## Testing

### Checklist Completo

#### Funcionalidad Core
- [ ] Login con credenciales correctas
- [ ] Login rechaza credenciales incorrectas
- [ ] Logout funciona
- [ ] Redirección a páginas correctas

#### ICT Assessment
- [ ] Formulario se renderiza correctamente
- [ ] Todos los campos funcionan
- [ ] Upload de archivos funciona
- [ ] Validación de campos requeridos
- [ ] Creación de carpeta con estructura correcta
- [ ] Archivos se copian a ubicación correcta
- [ ] HTML se genera correctamente
- [ ] Oportunidad se crea en Salesforce
- [ ] Mensajes de error apropiados

#### FCT Assessment
- [ ] (Mismo checklist que ICT)

#### IAT Assessment
- [ ] (Mismo checklist que ICT)

#### Integración
- [ ] Cuentas de Salesforce se cargan
- [ ] Navegación entre páginas
- [ ] Estado de sesión persiste
- [ ] No hay memory leaks

---

## Rollback

Si algo sale mal, puedes hacer rollback rápidamente:

### Rollback Completo

```bash
# 1. Restaurar main.py original
git checkout main.py

# 2. Restaurar assessment pages
git checkout pages/ict_assessment.py
git checkout pages/fct_assessment.py
git checkout pages/iat_assessment.py

# 3. Reiniciar Streamlit
# Ctrl+C y luego:
streamlit run main.py
```

### Rollback Parcial (Solo nuevas features)

Si solo quieres deshabilitar las nuevas features pero mantener mejoras:

```python
# En main.py, comentar imports nuevos
# from core.auth import AuthService
# from core.logging_config import setup_logging

# Descomentar código antiguo
# ... código original ...
```

---

## Próximos Pasos

### Corto Plazo
1. ✅ Migrar páginas de assessment
2. ⏳ Testing exhaustivo
3. ⏳ Deploy a ambiente de prueba

### Mediano Plazo
1. Implementar tests automatizados
2. Agregar logging a archivo
3. Configurar CI/CD

### Largo Plazo
1. Migrar a Microsoft Graph API / SharePoint
2. Implementar caché mejorado
3. Agregar métricas y monitoreo

---

## Soporte

Si encuentras problemas:

1. **Revisar logs:**
   ```python
   # Los logs ahora se imprimen en consola
   # Buscar mensajes ERROR o WARNING
   ```

2. **Verificar configuración:**
   ```bash
   python scripts/validate_config.py
   ```

3. **Rollback si es necesario** (ver sección anterior)

4. **Contactar al equipo de desarrollo**

---

## Recursos Adicionales

- `ANALYSIS_AND_REFACTORING.md` - Análisis completo de la refactorización
- `README.md` - Documentación general
- Código fuente con docstrings detallados
- Logs de la aplicación

---

**Última actualización:** Octubre 2025  
**Versión:** 2.0 (Refactorizada)
