# iBtest Assessment Application v2.0 (Refactored)

Una aplicación basada en Streamlit para gestionar evaluaciones de pruebas para iBtest. La aplicación permite a los usuarios enviar formularios de evaluación para diferentes tipos de pruebas: In Circuit Test (ICT), Functional Test (FCT) e Industrial Automation Test (IAT).

**🎉 Nueva versión refactorizada con arquitectura mejorada y preparada para Microsoft Graph API.**

---

## 🚀 Características

### Funcionalidad Principal
- ✅ **Múltiples Tipos de Evaluación**: Soporte para ICT, FCT e IAT
- ✅ **Validación de Formularios**: Validación completa de entradas
- ✅ **Carga de Archivos**: Soporte para múltiples tipos de archivos
- ✅ **Integración con Salesforce**: Creación automática de oportunidades
- ✅ **Reportes HTML**: Generación de reportes para cada evaluación
- ✅ **UI Responsiva**: Interfaz moderna y amigable

### Mejoras en v2.0 (Refactorizada)
- 🆕 **Configuración Centralizada**: Todas las settings en un solo lugar
- 🆕 **Autenticación Modular**: Sistema de auth reutilizable y testeable
- 🆕 **Abstracción de Almacenamiento**: Preparado para Microsoft Graph API
- 🆕 **Logging Estructurado**: Debugging y monitoreo mejorados
- 🆕 **Manejo de Errores Robusto**: Excepciones personalizadas
- 🆕 **Servicios de Negocio**: Lógica encapsulada y reutilizable
- 🆕 **Principios SOLID**: Arquitectura mantenible y extensible

---

## 📁 Estructura del Proyecto

```
sf-assessments/
├── main.py                          # Punto de entrada (refactorizado)
│
├── config/                          # 🆕 Configuración centralizada
│   ├── __init__.py
│   └── settings.py                  # Settings con validación
│
├── core/                            # 🆕 Funcionalidad core
│   ├── __init__.py
│   ├── auth.py                      # Servicio de autenticación
│   ├── exceptions.py                # Excepciones personalizadas
│   └── logging_config.py            # Configuración de logging
│
├── services/                        # 🆕 Lógica de negocio
│   ├── __init__.py
│   ├── salesforce_service.py        # Servicio Salesforce
│   └── storage_service.py           # Servicio de almacenamiento
│
├── storage/                         # 🆕 Abstracción de almacenamiento
│   ├── __init__.py
│   ├── base.py                      # Interface StorageProvider
│   ├── local_storage.py             # Implementación local
│   └── sharepoint_storage.py        # Implementación SharePoint
│
├── pages/                           # Páginas de evaluación
│   ├── ict_assessment.py            # Evaluación ICT
│   ├── fct_assessment.py            # Evaluación FCT
│   ├── iat_assessment.py            # Evaluación IAT
│   │
│   └── utils/                       # Módulos de utilidades
│       ├── base_assessment.py           # Clase base original
│       ├── base_assessment_refactored.py # 🆕 Versión mejorada
│       ├── constants.py                 # Constantes
│       ├── dates_info.py                # Utilidades de fechas
│       ├── global_styles.py             # Estilos globales CSS
│       ├── validations.py               # Validaciones
│       ├── *_create_html.py             # Generadores de HTML
│       ├── salesforce_access.py         # Acceso a Salesforce (legacy)
│       └── test_account_names.py        # Utilidades de cuentas
│
├── scripts/                         # 🆕 Scripts de utilidad
│   ├── validate_config.py           # Validador de configuración
│   └── generate_password_hash.py    # Generador de hash
│
├── 📚 Documentación
│   ├── ANALYSIS_AND_REFACTORING.md  # Análisis detallado
│   ├── MIGRATION_GUIDE.md           # Guía de migración
│   ├── REFACTORING_SUMMARY.md       # Resumen ejecutivo
│   └── .env.example                 # Template de configuración
│
├── .env                             # Variables de entorno (no en git)
├── .gitignore                       # Archivos ignorados
├── requirements.txt                 # Dependencias Python
├── logo_ibtest.png                  # Logo de iBtest
└── README.md                        # Este archivo
```

---

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- Cuenta de Salesforce con API habilitada
- Credenciales de Azure AD (para SharePoint - opcional)

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/yourusername/sf-assessments.git
   cd sf-assessments
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales
   ```

5. **Generar hash de contraseña:**
   ```bash
   python scripts/generate_password_hash.py
   # Copiar el hash a .env como APP_PASSWORD
   ```

6. **Validar configuración:**
   ```bash
   python scripts/validate_config.py
   ```

---

## ⚙️ Configuración

### Variables de Entorno Requeridas

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Salesforce
SALESFORCE_USERNAME=tu_usuario@empresa.com
SALESFORCE_PASSWORD=tu_contraseña
SALESFORCE_SECURITY_TOKEN=tu_token
SALESFORCE_CONSUMER_KEY=tu_consumer_key
SALESFORCE_CONSUMER_SECRET=tu_consumer_secret
TOKEN_URL=https://login.salesforce.com/services/oauth2/token
SF_TIMEOUT=30

# Almacenamiento
PATH_FILE=/ruta/a/archivos/locales
PATH_TO_SHAREPOINT=/ruta/sharepoint
TEMPLATE_ICT=/ruta/template/ict
TEMPLATE_FCT=/ruta/template/fct
TEMPLATE_IAT=/ruta/template/iat

# Autenticación
APP_PASSWORD=tu_hash_sha256
```

Ver `.env.example` para más detalles y opciones de SharePoint.

---

## 🚀 Uso

### Iniciar la Aplicación

```bash
streamlit run main.py
```

La aplicación se abrirá en `http://localhost:8501`

### Flujo de Trabajo

1. **Login:** Ingresar con credenciales proporcionadas
2. **Seleccionar Tipo de Evaluación:** ICT, FCT o IAT
3. **Llenar Formulario:** Completar todos los campos requeridos
4. **Cargar Archivos:** Subir documentos necesarios
5. **Enviar:** El sistema crea:
   - Carpeta de proyecto con archivos
   - Reporte HTML
   - Oportunidad en Salesforce

---

## 🏗️ Arquitectura

### Patrón de Diseño

La aplicación sigue una arquitectura en capas:

```
┌─────────────────────────────────────────┐
│         UI Layer (Streamlit)            │
│     (pages/*_assessment.py)             │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Business Logic Layer              │
│   (services/, BaseAssessment)           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Data Access Layer                 │
│  (storage/, SalesforceService)          │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      External Systems                   │
│  (Filesystem/SharePoint, Salesforce)    │
└─────────────────────────────────────────┘
```

### Principios SOLID Aplicados

- **Single Responsibility:** Cada clase tiene una única responsabilidad
- **Open/Closed:** Extensible sin modificar código existente
- **Liskov Substitution:** StorageProviders intercambiables
- **Interface Segregation:** Interfaces específicas
- **Dependency Inversion:** Depende de abstracciones

---

## 🧪 Testing

### Validar Configuración

```bash
python scripts/validate_config.py
```

### Tests Manuales

Ver checklist completo en `MIGRATION_GUIDE.md`

### Tests Automatizados (Futuro)

```bash
pytest tests/
```

---

## 📖 Desarrollo

### Agregar Nuevo Tipo de Evaluación

1. **Crear página de evaluación:**
   ```python
   # pages/new_assessment.py
   from pages.utils.base_assessment_refactored import BaseAssessment
   from core.auth import require_authentication
   
   @require_authentication
   def main():
       assessment = BaseAssessment(
           assessment_type="NEW",
           title="New Assessment",
           projects_folder="3_New_Assessment"
       )
       assessment.render_form(...)
   ```

2. **Crear generador HTML:**
   ```python
   # pages/utils/new_create_html.py
   def json_to_html(info):
       # Generar HTML del reporte
       pass
   ```

3. **Agregar ruta en main.py:**
   ```python
   page_routes = {
       # ...
       "new_assessment": "pages/new_assessment.py"
   }
   ```

### Mejores Prácticas

- ✅ Usar servicios existentes (SalesforceService, StorageService)
- ✅ Agregar logging apropiado
- ✅ Manejar excepciones específicas
- ✅ Documentar con docstrings
- ✅ Seguir convenciones de código existentes

---

## 🔄 Migración a SharePoint/Graph API

### Estado Actual
- ✅ Interface StorageProvider definida
- ✅ LocalStorageProvider funcional
- ✅ SharePointStorageProvider esqueleto
- ⏳ Pendiente: Implementación completa

### Pasos para Migrar

Ver guía completa en `MIGRATION_GUIDE.md` sección "Migración a Microsoft Graph API"

**Resumen:**
1. Configurar Azure AD App
2. Agregar variables de entorno Azure
3. Instalar `msal` (ya en requirements.txt)
4. Cambiar storage provider en código
5. Testing exhaustivo

---

## 📚 Documentación Adicional

- **`ANALYSIS_AND_REFACTORING.md`** - Análisis detallado de fortalezas y mejoras
- **`MIGRATION_GUIDE.md`** - Guía paso a paso para migración
- **`REFACTORING_SUMMARY.md`** - Resumen ejecutivo de cambios
- **`.env.example`** - Template de configuración

---

## 🔒 Seguridad

### Mejores Prácticas Implementadas

- ✅ Contraseñas hasheadas (SHA-256)
- ✅ Variables de entorno para credenciales
- ✅ `.env` en `.gitignore`
- ✅ Validación de emails corporativos
- ✅ Autenticación antes de cada página
- ✅ Tokens OAuth para APIs

### Recomendaciones Adicionales

- 🔐 Rotar credenciales regularmente
- 🔐 Usar HTTPS en producción
- 🔐 Implementar rate limiting
- 🔐 Auditar accesos
- 🔐 Backup de datos regularmente

---

## 🐛 Troubleshooting

### Error: "Required environment variable not set"

**Solución:**
```bash
python scripts/validate_config.py
# Revisar qué variables faltan y agregarlas a .env
```

### Error: "Failed to connect to Salesforce"

**Verificar:**
- Username y password correctos
- Security token válido
- Consumer key/secret correctos
- Red/firewall no bloquea conexión

### Error: "Folder already exists"

**Causa:** Proyecto con mismo nombre ya existe

**Solución:** Usar nombre diferente o contactar Sales Manager

### Error: Storage/Upload issues

**Verificar:**
- PATH_FILE existe y tiene permisos de escritura
- Templates existen en rutas configuradas
- Espacio en disco suficiente

---

## 🤝 Contribuir

### Reporte de Bugs

1. Verificar que no esté ya reportado
2. Incluir pasos para reproducir
3. Incluir logs relevantes
4. Incluir versión de Python y dependencias

### Pull Requests

1. Fork el repositorio
2. Crear branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📝 Changelog

### v2.0 (Octubre 2025) - Refactorización Mayor
- ✨ Configuración centralizada con validación
- ✨ Autenticación modular con decoradores
- ✨ Abstracción de almacenamiento (preparado para Graph API)
- ✨ Servicios de negocio encapsulados
- ✨ Logging estructurado
- ✨ Excepciones personalizadas
- ✨ Documentación completa
- ✨ Scripts de utilidad

### v1.0 - Versión Original
- ✅ Evaluaciones ICT, FCT, IAT
- ✅ Integración con Salesforce
- ✅ Carga de archivos
- ✅ Generación de reportes HTML
- ✅ UI responsiva

---

## 📄 Licencia

Este proyecto es propietario y confidencial. Está prohibida la copia, distribución o uso no autorizado.

---

## 👥 Contacto

Para preguntas o soporte, contactar al equipo de iBtest.

---

## 🙏 Agradecimientos

- Streamlit por el excelente framework
- Simple-Salesforce por la integración con Salesforce
- Comunidad Python por las librerías

---

**Versión:** 2.0 (Refactorizada)  
**Última actualización:** Octubre 2025  
**Estado:** ✅ Producción Ready (con opción de rollback a v1.0)
