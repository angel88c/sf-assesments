# 🚀 Despliegue en Streamlit Community Cloud

## 📋 Resumen

Esta aplicación soporta dos entornos:
- **Desarrollo Local:** Usa archivo `.env`
- **Streamlit Cloud:** Usa `.streamlit/secrets.toml`

El código detecta automáticamente el entorno y lee la configuración apropiada.

---

## 🔧 Configuración por Entorno

### **Desarrollo Local** (Ya configurado ✅)

```bash
# Tu archivo .env funciona perfectamente
.env                    # ← Configuración local (ignorado por Git)
```

**No necesitas cambiar nada para desarrollo local.**

---

### **Streamlit Community Cloud** (Nueva configuración)

#### **Paso 1: Crear archivo secrets.toml**

```bash
# Copia el template
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

#### **Paso 2: Editar secrets.toml con tus credenciales**

```bash
# Edita el archivo
nano .streamlit/secrets.toml
```

**Estructura del archivo `secrets.toml`:**

```toml
# Streamlit Cloud Secrets Configuration

[salesforce]
username = "tu_usuario@empresa.com"
password = "tu_password"
security_token = "tu_security_token"
consumer_key = "tu_consumer_key"
consumer_secret = "tu_consumer_secret"
token_url = "https://login.salesforce.com/services/oauth2/token"
timeout = 40

[storage]
provider = "sharepoint"
path_file = "/tmp"  # No usado en cloud, pero requerido
path_to_sharepoint = "https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos compartidos"
template_ict = "/tmp/TEMPLATE_ICT"  # No usado en cloud
template_fct = "/tmp/TEMPLATE_FCT"  # No usado en cloud
template_iat = "/tmp/TEMPLATE_IAT"  # No usado en cloud

[sharepoint]
base_path = "01_2025"
tenant_id = "58fc66f3-5586-4967-8302-03dc2a2f6513"
client_id = "d779dfb6-8dfd-459d-9403-3a84b9f241eb"
client_secret = "TU_NUEVO_CLIENT_SECRET"  # ⚠️ USA EL NUEVO (rotado)
site_id = "ibtest2020.sharepoint.com,0670681a-c391-4a3d-bc9b-e0f0b1b8dd09,d9c99339-198d-44e3-aae0-fc56e347e583"
drive_id = "b!GmhwBpHDPUq8m-DwsbjdCTmTydmNGeNEquD8VuNH5YPzUjP8TwwYQKr_-8K5CDm9"

[auth]
password_hash = "TU_SHA256_PASSWORD_HASH"

[logging]
level = "INFO"
```

---

## 🌐 Despliegue en Streamlit Community Cloud

### **Paso 1: Subir código a GitHub**

```bash
# Ya está hecho ✅
git push origin main
```

### **Paso 2: Ir a Streamlit Community Cloud**

1. Ve a https://share.streamlit.io/
2. Click en "New app"
3. Conecta tu repositorio GitHub: `angel88c/sf-assesments`
4. Selecciona:
   - **Branch:** `main`
   - **Main file path:** `main.py`
5. Click en "Advanced settings"

### **Paso 3: Configurar Secrets en Streamlit Cloud**

En la sección "Secrets", copia TODO el contenido de tu archivo local `.streamlit/secrets.toml`:

```toml
# Copia TODO desde tu archivo secrets.toml local
[salesforce]
username = "..."
password = "..."
# ... (todo el contenido)
```

### **Paso 4: Deploy**

Click en "Deploy!" y espera a que se despliegue.

---

## 🔍 Cómo Funciona la Detección Automática

### **En `config/settings.py`:**

```python
@classmethod
def _is_streamlit_cloud(cls) -> bool:
    """Check if running on Streamlit Cloud."""
    return HAS_STREAMLIT and hasattr(st, 'secrets') and len(st.secrets) > 0
```

### **Flujo de Decisión:**

```
┌─────────────────────────────────┐
│ Aplicación inicia               │
└───────────┬─────────────────────┘
            │
            ▼
    ¿Existe st.secrets?
            │
    ┌───────┴───────┐
    │               │
   SÍ              NO
    │               │
    ▼               ▼
Streamlit      Desarrollo
  Cloud          Local
    │               │
    ▼               ▼
Lee de          Lee de
secrets.toml    .env
```

---

## 📁 Estructura de Archivos

```
proyecto/
├── .env                           # ❌ Git ignore - Tu config local
├── .env.example.template          # ✅ En Git - Template público
├── .streamlit/
│   ├── secrets.toml              # ❌ Git ignore - Tu config cloud
│   └── secrets.toml.example      # ✅ En Git - Template público
├── config/
│   └── settings.py               # ✅ Detecta automáticamente el entorno
└── main.py                       # ✅ Entry point
```

---

## ⚙️ Variables de Configuración

### **Mapeo: .env ↔ secrets.toml**

| Variable .env | secrets.toml | Descripción |
|---------------|--------------|-------------|
| `SALESFORCE_USERNAME` | `[salesforce].username` | Usuario Salesforce |
| `SALESFORCE_PASSWORD` | `[salesforce].password` | Password Salesforce |
| `SALESFORCE_SECURITY_TOKEN` | `[salesforce].security_token` | Security token |
| `SALESFORCE_CONSUMER_KEY` | `[salesforce].consumer_key` | Consumer key |
| `SALESFORCE_CONSUMER_SECRET` | `[salesforce].consumer_secret` | Consumer secret |
| `SF_TIMEOUT` | `[salesforce].timeout` | Timeout (segundos) |
| `STORAGE_PROVIDER` | `[storage].provider` | "local" o "sharepoint" |
| `PATH_TO_SHAREPOINT` | `[storage].path_to_sharepoint` | URL SharePoint |
| `AZURE_TENANT_ID` | `[sharepoint].tenant_id` | Azure Tenant ID |
| `AZURE_CLIENT_ID` | `[sharepoint].client_id` | Azure Client ID |
| `AZURE_CLIENT_SECRET` | `[sharepoint].client_secret` | Azure Client Secret |
| `SHAREPOINT_SITE_ID` | `[sharepoint].site_id` | SharePoint Site ID |
| `SHAREPOINT_DRIVE_ID` | `[sharepoint].drive_id` | SharePoint Drive ID |
| `SHAREPOINT_BASE_PATH` | `[sharepoint].base_path` | Base path (ej: "01_2025") |
| `APP_PASSWORD` | `[auth].password_hash` | Password hash SHA-256 |

---

## ✅ Checklist de Despliegue

### **Antes de Desplegar:**

- [ ] **Rotar Azure Client Secret** (el anterior fue expuesto en Git)
- [ ] Crear `.streamlit/secrets.toml` local
- [ ] Copiar valores de `.env` a `secrets.toml`
- [ ] Usar el NUEVO client secret rotado
- [ ] Verificar que todos los secrets están completos
- [ ] Probar localmente (la app debe seguir funcionando con `.env`)

### **En Streamlit Cloud:**

- [ ] Crear nueva app en https://share.streamlit.io/
- [ ] Seleccionar repositorio `angel88c/sf-assesments`
- [ ] Configurar `main.py` como archivo principal
- [ ] Pegar secrets.toml en la configuración
- [ ] Deploy
- [ ] Probar que funciona correctamente

### **Después del Despliegue:**

- [ ] Verificar que la app carga correctamente
- [ ] Probar login
- [ ] Crear un assessment de prueba
- [ ] Verificar conexión a Salesforce
- [ ] Verificar subida a SharePoint
- [ ] Eliminar assessment de prueba

---

## 🐛 Troubleshooting

### **Error: "Required secret not found"**

**Causa:** Falta una variable en `secrets.toml` de Streamlit Cloud

**Solución:**
1. Ve a tu app en Streamlit Cloud
2. Click en "⋮" → "Settings" → "Secrets"
3. Agrega la variable faltante
4. Guarda y redeploy

### **Error: "Failed to connect to Salesforce"**

**Causa:** Credenciales incorrectas en secrets.toml

**Solución:**
1. Verifica usuario, password y security token
2. Verifica consumer key y secret
3. Actualiza secrets en Streamlit Cloud

### **Error: "Azure authentication failed"**

**Causa:** Client secret incorrecto o expirado

**Solución:**
1. Verifica que usas el NUEVO client secret (rotado)
2. Ve a Azure Portal → App registrations
3. Verifica que el secret no haya expirado
4. Genera nuevo secret si es necesario
5. Actualiza secrets.toml

### **App funciona local pero no en cloud**

**Causas posibles:**
1. Secrets mal configurados en Streamlit Cloud
2. Formato incorrecto en secrets.toml
3. Falta alguna sección ([salesforce], [storage], etc.)

**Solución:**
1. Compara tu `secrets.toml` local con el de Streamlit Cloud
2. Verifica que todas las secciones existan
3. Verifica que no haya espacios extra o caracteres especiales
4. Redeploy después de corregir

---

## 🔐 Seguridad

### **❌ NUNCA subas a Git:**
- `.env`
- `.streamlit/secrets.toml`
- Cualquier archivo con credenciales reales

### **✅ Seguro para Git:**
- `.env.example.template`
- `.streamlit/secrets.toml.example`
- Código fuente
- Documentación

### **Verificación:**

```bash
# Verifica que secrets.toml NO está en Git
git ls-files | grep secrets.toml

# No debería retornar nada excepto:
# .streamlit/secrets.toml.example
```

---

## 📚 Referencias

- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Deploy Streamlit Apps](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

---

## 🎉 Resumen

| Entorno | Archivo Config | Ubicación | Git |
|---------|----------------|-----------|-----|
| **Local** | `.env` | Local filesystem | ❌ Ignorado |
| **Cloud** | `secrets.toml` | Streamlit dashboard | ❌ Ignorado |
| **Template** | `.env.example.template` | Repositorio | ✅ En Git |
| **Template** | `secrets.toml.example` | Repositorio | ✅ En Git |

**La aplicación detecta automáticamente dónde está corriendo y usa la configuración apropiada.** 🚀
