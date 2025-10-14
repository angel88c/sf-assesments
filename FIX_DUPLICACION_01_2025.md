# ✅ FIX: Duplicación de 01_2025 en SharePoint

## 🐛 Problema

Al crear proyectos en SharePoint con `SHAREPOINT_BASE_PATH=01_2025`, se creaban con ruta duplicada:

```
❌ ANTES:
01_2025/01_2025/1_In_Circuit Test (ICT)/MX/Cliente/Proyecto
```

## 🔍 Causa Raíz

El problema ocurría en el método `copy_template()` de `SharePointStorageProvider`:

1. **`project_path` ya incluía `base_path`** (01_2025) desde `get_full_path()`
2. Pero `copy_template()` llamaba a `create_folder()` y `upload_file()`
3. Estos métodos internamente llamaban a `_get_item_path()` 
4. `_get_item_path()` **volvía a agregar `base_path`** → duplicación

```python
# Flujo problemático:
project_path = "01_2025/1_ICT/MX/..."  # Ya incluye base_path
  ↓
copy_template(template, project_path)
  ↓
  create_folder(sharepoint_path)  # sharepoint_path = "01_2025/1_ICT/..."
    ↓
    _get_item_path(path)  # Agrega base_path de nuevo
      ↓
      return "01_2025/" + path  # ❌ Duplicación: 01_2025/01_2025/...
```

## ✅ Solución

Creé métodos internos `_create_folder_raw()` y `_upload_file_raw()` que **NO** agregan `base_path`:

### **Archivos Modificados:**

#### 1. `storage/sharepoint_storage.py`

**Agregados:**
- `_create_folder_raw(path)` - Crea carpeta sin agregar base_path
- `_upload_file_raw(content, destination, filename)` - Sube archivo sin agregar base_path

**Modificados:**
- `create_folder(path)` - Ahora llama a `_create_folder_raw(_get_item_path(path))`
- `upload_file(content, destination, filename)` - Ahora llama a `_upload_file_raw()`
- `upload_files(files, destination)` - Usa `_upload_file_raw()` para evitar duplicación
- `write_file(content, destination, filename)` - Usa `_upload_file_raw()` para evitar duplicación
- `copy_template(template, destination)` - Usa métodos `_raw` en lugar de los públicos

### **Cambios Clave:**

```python
# ANTES (en copy_template, write_file, upload_files):
self.create_folder(sharepoint_path)  # ❌ Agregaba base_path de nuevo
self.upload_file(content, destination, filename)  # ❌ Agregaba base_path de nuevo

# DESPUÉS:
self._create_folder_raw(sharepoint_path)  # ✅ Usa path directo
self._upload_file_raw(content, destination, filename)  # ✅ Usa path directo
```

## 📊 Resultado

### **✅ DESPUÉS:**
```
01_2025/1_In_Circuit Test (ICT)/MX/Cliente/Proyecto
```

Solo aparece `01_2025` una vez, en la ubicación correcta.

## 🧪 Verificación

### **Test Exitoso:**
```bash
python3 test_sharepoint_base_path.py
```

Resultado:
```
✅ '01_2025' aparece 1 vez/veces
✅ Correcto: sin duplicación
🎉 ¡PERFECTO! Path coincide con lo esperado
```

### **Logs de Creación:**
```
Created folder: 01_2025/1_In_Circuit Test (ICT)/MX/...
Uploaded file: 01_2025/1_In_Circuit Test (ICT)/MX/.../file.xlsx
```

Ya no muestra `01_2025/01_2025/...`

## 📋 Estructura Final en SharePoint

```
Documentos compartidos/
  └── 01_2025/  ← Solo una vez
      ├── 1_In_Circuit_Test_(ICT)/
      │   ├── MX/
      │   │   └── Cliente/
      │   │       └── Proyecto/
      │   │           ├── 1_Customer_Info/
      │   │           ├── 2_BOM/
      │   │           └── ...
      ├── 2_Functional_Test_(FCT)/
      └── 4_Industrial_Automation_(IAT)/
```

## 🔧 Configuración en .env

```bash
# URL base de SharePoint (para Salesforce)
PATH_TO_SHAREPOINT=https://ibtest2020.sharepoint.com/sites/Public_Quotes_2025/Documentos compartidos

# Carpeta base DENTRO de SharePoint
SHAREPOINT_BASE_PATH=01_2025

# Storage provider
STORAGE_PROVIDER=sharepoint
```

## ✅ Resumen de Métodos

| Método | Agrega `base_path`? | Uso |
|--------|---------------------|-----|
| `_get_item_path(path)` | ✅ Sí | Helper interno |
| `_create_folder_raw(path)` | ❌ No | Usado internamente cuando path ya incluye base_path |
| `_upload_file_raw(...)` | ❌ No | Usado internamente cuando path ya incluye base_path |
| `create_folder(path)` | ✅ Sí (vía `_get_item_path`) | API pública |
| `upload_file(...)` | ✅ Sí (vía `_get_item_path`) | API pública |
| `upload_files(...)` | ❌ No (usa `_raw` internamente) | Sube múltiples archivos |
| `write_file(...)` | ❌ No (usa `_raw` internamente) | Escribe archivo de texto (ej: HTML) |
| `copy_template(...)` | ❌ No (usa métodos `_raw`) | Copia template completo |

## 🚀 Para Usar

1. **Reinicia la aplicación:**
   ```bash
   streamlit run main.py
   ```

2. **Crea un assessment**

3. **Verifica en SharePoint:**
   - Carpeta: `01_2025/1_ICT/MX/Cliente/Proyecto`
   - Sin duplicación ✅

4. **Verifica URL en Salesforce:**
   - `https://.../Documentos compartidos/01_2025/1_ICT/MX/Cliente/Proyecto`
   - Click funciona directamente ✅

## 🎉 Estado: CORREGIDO

El problema de duplicación está completamente resuelto. Los proyectos se crean correctamente con la estructura:

```
01_2025/[tipo_assessment]/[país]/[cliente]/[proyecto]
```

Sin ninguna duplicación de `01_2025`.
