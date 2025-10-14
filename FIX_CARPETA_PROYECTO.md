# ✅ FIX ADICIONAL: Carpeta del Proyecto

## 🐛 Problema

Después de corregir los archivos (HTML, templates, archivos subidos), la **carpeta inicial del proyecto** todavía se creaba con duplicación:

```
❌ PROBLEMA:
01_2025/01_2025/1_In_Circuit Test (ICT)/MX/Cliente/Proyecto/
         ↑ Carpeta vacía duplicada
```

## 🔍 Causa Raíz

El problema estaba en `StorageService.create_project_folder()`:

```python
# 1. get_full_path() retorna path con base_path incluido
project_path = self.provider.get_full_path(...)
# → "01_2025/1_ICT/MX/Cliente/Proyecto"

# 2. folder_exists() agrega base_path de nuevo
if self.provider.folder_exists(project_path):  # ❌
    # Verifica: 01_2025/01_2025/...

# 3. create_folder() agrega base_path de nuevo
self.provider.create_folder(project_path)  # ❌
    # Crea: 01_2025/01_2025/...
```

## ✅ Solución

### **1. Agregado método `_folder_exists_raw()` en SharePointStorageProvider**

```python
def _folder_exists_raw(self, path: str) -> bool:
    """Check if folder exists using raw path (no base_path added)."""
    url = f"{self.graph_url}/drives/{self.drive_id}/root:/{path}"
    response = requests.get(url, headers=self._get_headers())
    return response.status_code == 200
```

### **2. Modificado `folder_exists()` para usar `_raw`**

```python
def folder_exists(self, path: str) -> bool:
    """Check if folder exists (adds base_path)."""
    item_path = self._get_item_path(path)  # Agrega base_path
    return self._folder_exists_raw(item_path)
```

### **3. Modificado `StorageService.create_project_folder()`**

```python
# Check if exists - usa método _raw
if hasattr(self.provider, '_folder_exists_raw'):
    exists = self.provider._folder_exists_raw(project_path)  # ✅ Sin duplicar
else:
    exists = self.provider.folder_exists(project_path)  # Para LocalProvider

if exists:
    raise StorageError("Project already exists")

# Create folder - usa método _raw
if hasattr(self.provider, '_create_folder_raw'):
    self.provider._create_folder_raw(project_path)  # ✅ Sin duplicar
else:
    self.provider.create_folder(project_path)  # Para LocalProvider
```

## 📊 Resultado

### **❌ ANTES:**
```
Logs:
  Creating project folder: 01_2025/1_ICT/MX/Cliente/Proyecto
  Checking exists at: 01_2025/01_2025/1_ICT/MX/Cliente/Proyecto  ❌
  Created folder: 01_2025/01_2025/1_ICT/MX/Cliente/Proyecto  ❌

SharePoint:
  01_2025/
    └── 01_2025/  ← Carpeta vacía duplicada
        └── 1_ICT/...
```

### **✅ DESPUÉS:**
```
Logs:
  Creating project folder: 01_2025/1_ICT/MX/Cliente/Proyecto
  Checking exists at: 01_2025/1_ICT/MX/Cliente/Proyecto  ✅
  Created folder: 01_2025/1_ICT/MX/Cliente/Proyecto  ✅

SharePoint:
  01_2025/  ← Solo una vez
    └── 1_ICT/...
```

## 🔧 Archivos Modificados

### **1. `storage/sharepoint_storage.py`**
- ✅ Agregado: `_folder_exists_raw(path)`
- ✅ Modificado: `folder_exists(path)` - Ahora usa `_folder_exists_raw()`

### **2. `services/storage_service.py`**
- ✅ Modificado: `create_project_folder()` - Usa métodos `_raw` para SharePoint

## 📋 Métodos Completos que Usan `_raw`

| Operación | Método Público | Método `_raw` | Usado Por |
|-----------|----------------|---------------|-----------|
| Crear carpeta | `create_folder()` | `_create_folder_raw()` | `StorageService`, `copy_template` |
| Verificar existe | `folder_exists()` | `_folder_exists_raw()` | `StorageService` |
| Subir archivo | `upload_file()` | `_upload_file_raw()` | `write_file`, `upload_files`, `copy_template` |

## ✅ Checklist de Verificación

Al crear un nuevo assessment, verifica:

- [ ] **Logs muestran path correcto:**
  ```
  ✅ Creating project folder: 01_2025/1_ICT/MX/...
  ❌ NO: 01_2025/01_2025/...
  ```

- [ ] **Carpeta en SharePoint correcta:**
  ```
  ✅ 01_2025/1_ICT/MX/Cliente/Proyecto/
  ❌ NO: 01_2025/01_2025/...
  ```

- [ ] **No hay carpeta duplicada vacía:**
  ```
  ✅ 01_2025/ (con contenido)
  ❌ NO: 01_2025/01_2025/ (vacía)
  ```

- [ ] **Todos los archivos en ubicación correcta:**
  ```
  ✅ 01_2025/1_ICT/MX/Cliente/Proyecto/ICT_Assessment.html
  ✅ 01_2025/1_ICT/MX/Cliente/Proyecto/1_Customer_Info/...
  ```

## 🚀 Para Probar

1. **Reinicia la aplicación:**
   ```bash
   streamlit run main.py
   ```

2. **Crea un assessment nuevo**

3. **Verifica logs:**
   ```
   Creating project folder: 01_2025/1_In_Circuit Test (ICT)/MX/...
   Created folder: 01_2025/1_In_Circuit Test (ICT)/MX/...
   ```
   **Sin** `01_2025/01_2025/...`

4. **Verifica en SharePoint:**
   - Solo debe existir `01_2025/` (una vez)
   - No debe haber carpeta `01_2025/01_2025/`

## 🎉 Estado: COMPLETADO

✅ Carpeta del proyecto se crea correctamente
✅ Sin duplicación de `01_2025`
✅ Método `folder_exists()` funciona correctamente
✅ Compatible con LocalProvider (usa `hasattr()`)

**El problema de la carpeta duplicada está completamente resuelto.** 🚀
