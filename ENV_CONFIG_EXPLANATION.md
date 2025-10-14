# 📋 Explicación de Configuración .env para SharePoint

## 🎯 Resumen Conceptual

**PATH_FILE** = Rutas LOCALES (tu máquina)
**SharePoint** = Se maneja vía Graph API (no usa rutas locales)

---

## ⚙️ Variables en .env

### 1️⃣ **PATH_FILE** (Ruta LOCAL)
```bash
PATH_FILE=/Users/c_angel/Documents/iBtest/Projects
```

**Propósito:**
- ✅ Templates están en tu máquina local
- ✅ Cuando `STORAGE_PROVIDER=local`, carpetas se crean aquí
- ❌ NO se usa cuando `STORAGE_PROVIDER=sharepoint`

**Ejemplo:**
```
/Users/c_angel/Documents/iBtest/Projects/
  ├── TEMPLATE_ICT/
  ├── TEMPLATE_FCT/
  └── TEMPLATE_IAT/
```

---

### 2️⃣ **PATH_TO_SHAREPOINT** (URL de SharePoint)
```bash
PATH_TO_SHAREPOINT=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos
```

**Propósito:**
- ✅ URL base para generar links en Salesforce
- ✅ Se concatena con la ruta del proyecto
- ✅ Usuarios hacen click y abren carpeta en SharePoint

**Resultado en Salesforce:**
```
Path__c = https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos/1_ICT/MX/ACME/Project_001
```

---

### 3️⃣ **STORAGE_PROVIDER** (Dónde se crean las carpetas)
```bash
STORAGE_PROVIDER=sharepoint   # o 'local'
```

**Si = `local`:**
- Carpetas se crean en `PATH_FILE`
- Usa `os.makedirs()`, `shutil.copytree()`
- Filesystem local

**Si = `sharepoint`:**
- Carpetas se crean en SharePoint
- Usa Graph API (HTTP requests)
- No usa `PATH_FILE` para crear carpetas

---

### 4️⃣ **Configuración SharePoint** (Solo si STORAGE_PROVIDER=sharepoint)
```bash
AZURE_TENANT_ID=58fc66f3-5586-4967-8302-03dc2a2f6513
AZURE_CLIENT_ID=d779dfb6-8dfd-459d-9403-3a84b9f241eb
AZURE_CLIENT_SECRET=lwD8Q~KinaJmvTuM.tWb9Tj1LhQE~tf2J2NXkbkU

SHAREPOINT_SITE_ID=ibtest2020.sharepoint.com,0670681a-c391-4a3d-bc9b-e0f0b1b8dd09,d9c99339-198d-44e3-aae0-fc56e347e583
SHAREPOINT_DRIVE_ID=b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9
```

**Propósito:**
- Autenticación con Azure AD
- Acceso a SharePoint vía Graph API
- Crear/leer carpetas y archivos

---

## 🔄 Flujo Completo

### **Cuando STORAGE_PROVIDER=sharepoint**

```
1. Usuario llena assessment (ICT)
   Cliente: ACME Corp
   País: Mexico
   Proyecto: Test_001

2. StorageService detecta: provider = sharepoint

3. SharePointStorageProvider:
   - Autentica con Azure (AZURE_TENANT_ID, CLIENT_ID, SECRET)
   - Accede a SharePoint (SHAREPOINT_SITE_ID, DRIVE_ID)
   - Crea carpeta: 1_ICT/MX/ACME_Corp/Test_001
   - Copia template desde PATH_FILE (local) a SharePoint

4. Genera URL para Salesforce:
   base = PATH_TO_SHAREPOINT
   path = 1_ICT/MX/ACME_Corp/Test_001
   URL = base + path
   
5. Crea oportunidad en Salesforce:
   Path__c = URL completa
```

---

## ✅ Configuración Correcta para SharePoint

```bash
# ============================================================================
# STORAGE CONFIGURATION
# ============================================================================
# Ruta LOCAL para templates (NO cambia)
PATH_FILE=/Users/c_angel/Documents/iBtest/Projects

# Templates LOCALES (NO cambian)
TEMPLATE_ICT=/Users/c_angel/Documents/iBtest/Projects/TEMPLATE_ICT
TEMPLATE_FCT=/Users/c_angel/Documents/iBtest/Projects/TEMPLATE_FCT
TEMPLATE_IAT=/Users/c_angel/Documents/iBtest/Projects/TEMPLATE_IAT

# URL de SharePoint para links en Salesforce
PATH_TO_SHAREPOINT=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos

# ============================================================================
# SHAREPOINT CONFIGURATION (Dónde se CREAN las carpetas)
# ============================================================================
# Provider: local o sharepoint
STORAGE_PROVIDER=sharepoint

# Azure AD (para autenticación)
AZURE_TENANT_ID=58fc66f3-5586-4967-8302-03dc2a2f6513
AZURE_CLIENT_ID=d779dfb6-8dfd-459d-9403-3a84b9f241eb
AZURE_CLIENT_SECRET=lwD8Q~KinaJmvTuM.tWb9Tj1LhQE~tf2J2NXkbkU

# SharePoint (drive específico)
SHAREPOINT_SITE_ID=ibtest2020.sharepoint.com,0670681a-c391-4a3d-bc9b-e0f0b1b8dd09,d9c99339-198d-44e3-aae0-fc56e347e583
SHAREPOINT_DRIVE_ID=b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9
```

---

## ❌ Error Común

**INCORRECTO:**
```bash
# ❌ NO puedes poner una URL de SharePoint en PATH_FILE
PATH_FILE=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos
```

**¿Por qué no funciona?**
- `os.path.join(PATH_FILE, "ICT", "MX")` no funciona con URLs
- Templates locales no pueden leerse desde SharePoint con rutas
- `shutil.copytree()` no funciona con URLs HTTP

**CORRECTO:**
```bash
# ✅ PATH_FILE sigue siendo local
PATH_FILE=/Users/c_angel/Documents/iBtest/Projects

# ✅ SharePoint se maneja con provider y configuración separada
STORAGE_PROVIDER=sharepoint
AZURE_TENANT_ID=...
SHAREPOINT_SITE_ID=...
```

---

## 🧪 Verificación

### **Test 1: Verificar configuración**
```bash
python3 test_provider_auto_detection.py
```

Debe mostrar:
```
✅ Storage provider configurado: sharepoint
✅ Provider detectado: SharePointStorageProvider
```

### **Test 2: Crear proyecto de prueba**
```bash
python3 test_full_assessment_flow.py
```

Debe crear carpeta en SharePoint y generar URL correcta.

---

## 📚 Resumen

| Variable | Valor | Propósito |
|----------|-------|-----------|
| `PATH_FILE` | Ruta LOCAL | Templates + base local si provider=local |
| `PATH_TO_SHAREPOINT` | URL SharePoint | Base para URLs en Salesforce |
| `STORAGE_PROVIDER` | `sharepoint` o `local` | Dónde crear carpetas |
| `AZURE_*` | Credenciales | Autenticación con Azure |
| `SHAREPOINT_*` | IDs | Identificar site y drive en SharePoint |

**Clave:** PATH_FILE NO cambia. SharePoint se maneja con Graph API usando AZURE y SHAREPOINT variables.
