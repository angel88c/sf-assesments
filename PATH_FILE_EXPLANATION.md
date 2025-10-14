# 📋 Explicación Completa: PATH_FILE y SharePoint

## 🎯 Resumen Ejecutivo

**PATH_FILE ya NO se usa cuando `STORAGE_PROVIDER=sharepoint`**

---

## 📊 Uso de PATH_FILE

### **Con STORAGE_PROVIDER=local** (Código viejo)
```python
# Se crea carpeta en filesystem local
PATH_FILE = "/Users/c_angel/Documents/iBtest/Projects"

# Carpetas se crean en:
/Users/c_angel/Documents/iBtest/Projects/1_ICT/MX/Cliente/Proyecto/
```

### **Con STORAGE_PROVIDER=sharepoint** (Código nuevo)
```python
# PATH_FILE YA NO SE USA para crear carpetas
# Solo se requiere en config.py (legacy)

# Carpetas se crean EN SHAREPOINT vía Graph API
# Ubicación: SharePoint/Documentos/...
```

---

## ✅ Configuración Correcta en .env

```bash
# ============================================================================
# STORAGE - FILESYSTEM LOCAL (Para compatibilidad legacy)
# ============================================================================
# PATH_FILE ya no se usa con SharePoint, pero se requiere en config
# Puedes dejarlo apuntando a tu carpeta de templates
PATH_FILE=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES

# Templates (estos SÍ se usan - se leen localmente)
TEMPLATE_ICT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_ICT
TEMPLATE_FCT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_FCT
TEMPLATE_IAT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_IAT

# URL de SharePoint para links en Salesforce
PATH_TO_SHAREPOINT=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos

# ============================================================================
# STORAGE PROVIDER
# ============================================================================
STORAGE_PROVIDER=sharepoint

# ============================================================================
# SHAREPOINT CONFIGURATION
# ============================================================================
# Azure AD
AZURE_TENANT_ID=58fc66f3-5586-4967-8302-03dc2a2f6513
AZURE_CLIENT_ID=d779dfb6-8dfd-459d-9403-3a84b9f241eb
AZURE_CLIENT_SECRET=lwD8Q~KinaJmvTuM.tWb9Tj1LhQE~tf2J2NXkbkU

# SharePoint
SHAREPOINT_SITE_ID=ibtest2020.sharepoint.com,0670681a-c391-4a3d-bc9b-e0f0b1b8dd09,d9c99339-198d-44e3-aae0-fc56e347e583
SHAREPOINT_DRIVE_ID=b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9

# ============================================================================
# SHAREPOINT BASE PATH (Opcional)
# ============================================================================
# Prefijo DENTRO de SharePoint donde se crean las carpetas
# Si quieres que todo se cree dentro de "01_2025/", descomenta:
# SHAREPOINT_BASE_PATH=01_2025

# Si lo dejas vacío, las carpetas se crean en la raíz de Documentos:
SHAREPOINT_BASE_PATH=
```

---

## 🔄 Comparación: CON vs SIN SHAREPOINT_BASE_PATH

### **Sin SHAREPOINT_BASE_PATH (vacío)**
```
SharePoint → Documentos/
  ├── 1_In_Circuit_Test_(ICT)/
  │   ├── MX/
  │   │   └── ACME_Corp/
  │   │       └── Project_001/
  ├── 2_Functional_Test_(FCT)/
  └── 4_Industrial_Automation_(IAT)/
```

### **Con SHAREPOINT_BASE_PATH=01_2025**
```
SharePoint → Documentos/
  └── 01_2025/  ← Prefijo
      ├── 1_In_Circuit_Test_(ICT)/
      │   ├── MX/
      │   │   └── ACME_Corp/
      │   │       └── Project_001/
      ├── 2_Functional_Test_(FCT)/
      └── 4_Industrial_Automation_(IAT)/
```

---

## 🎯 Flujo Completo (SharePoint)

```
┌──────────────────────────────────────────────────────────┐
│ 1. Templates LOCALES                                     │
│    PATH_FILE = /Users/.../TEMPLATES (ya no se usa)      │
│                                                          │
│    TEMPLATE_ICT = /Users/.../TEMPLATES/TEMPLATE_ICT     │
│    TEMPLATE_FCT = /Users/.../TEMPLATES/TEMPLATE_FCT     │
│    TEMPLATE_IAT = /Users/.../TEMPLATES/TEMPLATE_IAT     │
│                                                          │
│    ✅ Se leen desde aquí                                │
└────────────┬─────────────────────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────────────────────┐
│ 2. StorageService detecta: STORAGE_PROVIDER=sharepoint  │
│    → Usa SharePointStorageProvider                       │
│    → base_path = SHAREPOINT_BASE_PATH (opcional)        │
└────────────┬─────────────────────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────────────────────┐
│ 3. SharePointStorageProvider                             │
│                                                          │
│    a) Autentica con Azure AD                            │
│       → AZURE_TENANT_ID, CLIENT_ID, SECRET              │
│                                                          │
│    b) Construye ruta en SharePoint:                     │
│       base_path + projects_folder + country + etc       │
│       Ejemplo: "01_2025/1_ICT/MX/ACME/Project_001"     │
│                                                          │
│    c) Crea carpeta EN SHAREPOINT (Graph API):           │
│       POST https://graph.microsoft.com/.../children     │
│                                                          │
│    d) Lee template LOCAL (TEMPLATE_ICT):                │
│       for file in /Users/.../TEMPLATE_ICT/*:            │
│                                                          │
│    e) Sube archivos A SHAREPOINT (Graph API):           │
│       PUT https://graph.microsoft.com/.../content       │
└────────────┬─────────────────────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────────────────────┐
│ 4. Resultado en SharePoint                               │
│                                                          │
│    SharePoint/Documentos/01_2025/                       │
│      └── 1_ICT/MX/ACME_Corp/Project_001/               │
│          ├── 1_Customer_Info/                           │
│          ├── 2_BOM/                                     │
│          └── ... (template completo)                    │
└────────────┬─────────────────────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────────────────────┐
│ 5. URL generada para Salesforce                         │
│                                                          │
│    PATH_TO_SHAREPOINT + project_path                    │
│    = https://.../Documentos/01_2025/1_ICT/.../Project  │
└──────────────────────────────────────────────────────────┘
```

---

## ❓ FAQ

### **P: ¿PATH_FILE se sigue necesitando?**
R: Sí, pero solo para compatibilidad con `config.py`. Si usas SharePoint, no se usa realmente.

### **P: ¿Puedo poner PATH_FILE como ruta de SharePoint?**
R: ❌ No, debe ser una ruta local porque:
- TEMPLATE_* se leen con `open(file, 'rb')`
- No puedes hacer `open("https://sharepoint.com/file")`

### **P: ¿Dónde se crean las carpetas con SharePoint?**
R: En SharePoint vía Graph API, NO en PATH_FILE:
- Base: `SHAREPOINT_DRIVE_ID` (Documentos)
- Prefijo opcional: `SHAREPOINT_BASE_PATH` (01_2025)
- Ruta completa: `01_2025/1_ICT/MX/Cliente/Proyecto`

### **P: ¿Para qué sirve SHAREPOINT_BASE_PATH?**
R: Para crear todas las carpetas dentro de un subfolder en SharePoint.
- Sin SHAREPOINT_BASE_PATH: `Documentos/1_ICT/MX/...`
- Con SHAREPOINT_BASE_PATH=01_2025: `Documentos/01_2025/1_ICT/MX/...`

### **P: ¿PATH_TO_SHAREPOINT es lo mismo que SHAREPOINT_BASE_PATH?**
R: No:
- `PATH_TO_SHAREPOINT`: URL para links en Salesforce
- `SHAREPOINT_BASE_PATH`: Prefijo de carpeta dentro de SharePoint

---

## ✅ Configuración Recomendada

```bash
# Filesystem local (solo para templates)
PATH_FILE=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES
TEMPLATE_ICT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_ICT
TEMPLATE_FCT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_FCT
TEMPLATE_IAT=/Users/c_angel/Documents/python/sf-assesments/TEMPLATES/TEMPLATE_IAT

# SharePoint
STORAGE_PROVIDER=sharepoint
PATH_TO_SHAREPOINT=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos
SHAREPOINT_BASE_PATH=  # Vacío = raíz, o "01_2025" para prefijo

# Azure & SharePoint IDs
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
SHAREPOINT_SITE_ID=...
SHAREPOINT_DRIVE_ID=...
```

---

## 🚀 ¡Listo para Usar!

Con esta configuración:
- ✅ Templates se leen desde carpeta local del proyecto
- ✅ Carpetas se crean en SharePoint vía Graph API
- ✅ URLs específicas se generan para Salesforce
- ✅ PATH_FILE ya no interfiere con SharePoint
