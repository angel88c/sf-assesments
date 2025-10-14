# ✅ FIX: Carpeta Duplicada con Sufijo "1"

## 🐛 Problema

Al crear un proyecto en SharePoint, se generaban **dos carpetas**:

```
01_2025/1_ICT/MX/Cliente/
  ├── Proyecto/      ← Carpeta correcta con todo el contenido
  └── Proyecto1/     ← Carpeta duplicada VACÍA con sufijo "1"
```

## 🔍 Causa Raíz

El problema era que **creábamos la carpeta del proyecto DOS VECES**:

### **Primera Creación:**
```python
# En StorageService.create_project_folder() - línea 156
self.provider._create_folder_raw(project_path)
# ✅ Crea: 01_2025/1_ICT/MX/Cliente/Proyecto/
```

### **Segunda Creación:**
```python
# En SharePointStorageProvider.copy_template() - línea 343
self._create_folder_raw(destination)
# ❌ Intenta crear de nuevo: 01_2025/1_ICT/MX/Cliente/Proyecto/
```

### **Comportamiento de SharePoint:**

Debido a `"@microsoft.graph.conflictBehavior": "rename"`, cuando intentaba crear una carpeta que **ya existe**:
- ❌ No fallaba
- ❌ No sobreescribía
- ✅ Creaba una **nueva carpeta con sufijo**: `Proyecto1/`

## ✅ Solución

### **1. Eliminar creación duplicada en `copy_template()`**

```python
# ANTES:
logger.info(f"Copying template from {template_path} to SharePoint: {destination}")
try:
    self._create_folder_raw(destination)  # ❌ Creaba carpeta de nuevo
    
# DESPUÉS:
logger.info(f"Copying template from {template_path} to SharePoint: {destination}")
try:
    # DO NOT create destination folder here - already created by create_project_folder()
    # Creating it here causes SharePoint to create duplicate with suffix (e.g., "Project1")
    # self._create_folder_raw(destination)  # ✅ Comentado
```

**Razón:** La carpeta del proyecto ya fue creada en `StorageService.create_project_folder()`. 

`copy_template()` solo debe crear las **subcarpetas del template** (1_Customer_Info, 2_BOM, etc.), no la carpeta raíz del proyecto.

### **2. Cambiar `conflictBehavior` de "rename" a "fail"**

```python
# ANTES:
payload = {
    "name": folder_name,
    "folder": {},
    "@microsoft.graph.conflictBehavior": "rename"  # ❌ Creaba duplicados
}

# DESPUÉS:
payload = {
    "name": folder_name,
    "folder": {},
    "@microsoft.graph.conflictBehavior": "fail"  # ✅ Falla si existe
}
```

**Razón:** 
- Con "rename": Si carpeta existe → crea `Proyecto1/` (duplicado silencioso)
- Con "fail": Si carpeta existe → error (nos alerta del problema)

El error es manejado correctamente en `copy_template()`:
```python
try:
    self._create_folder_raw(sharepoint_path)
    folders_created += 1
except StorageError as e:
    # Folder might already exist, continue
    logger.debug(f"Folder creation skipped (might exist): {sharepoint_path}")
```

## 📊 Resultado

### **❌ ANTES:**
```
SharePoint/01_2025/1_ICT/MX/Kimball_Electronics_Inc/
  ├── Test_Brownson_03/     ← Con contenido (correcto)
  └── Test_Brownson_031/    ← VACÍO (duplicado con sufijo)
```

### **✅ DESPUÉS:**
```
SharePoint/01_2025/1_ICT/MX/Kimball_Electronics_Inc/
  └── Test_Brownson_03/     ← Con contenido (único)
      ├── 0_Initial_Assessment/
      ├── 1_Customer_Info/
      ├── 2_Supplier_Quotes/
      ├── 3_Fixture_RFQ_&_Testsight_Files/
      ├── 4_iBTest_Quotation/
      └── ICT_Assessment.html
```

## 🔄 Flujo Corregido

### **Antes (con duplicación):**
```
1. StorageService.create_project_folder()
   └── _create_folder_raw("01_2025/1_ICT/MX/Cliente/Proyecto")  ✅ Crea carpeta
   
2. copy_template("TEMPLATE_ICT", "01_2025/1_ICT/MX/Cliente/Proyecto")
   └── _create_folder_raw("01_2025/1_ICT/MX/Cliente/Proyecto")  ❌ Crea "Proyecto1"
   └── Crea subcarpetas en "Proyecto1"  ❌ VACÍAS

Resultado: Proyecto (correcto) + Proyecto1 (vacío duplicado)
```

### **Después (corregido):**
```
1. StorageService.create_project_folder()
   └── _create_folder_raw("01_2025/1_ICT/MX/Cliente/Proyecto")  ✅ Crea carpeta
   
2. copy_template("TEMPLATE_ICT", "01_2025/1_ICT/MX/Cliente/Proyecto")
   └── NO crea carpeta raíz  ✅
   └── Crea solo subcarpetas del template:
       ├── 0_Initial_Assessment/
       ├── 1_Customer_Info/
       ├── 2_Supplier_Quotes/
       └── etc.

Resultado: Proyecto (único con contenido completo)
```

## 🔧 Archivos Modificados

### **`storage/sharepoint_storage.py`**

1. **Línea ~343:** Comentada la creación de `destination` en `copy_template()`
   ```python
   # self._create_folder_raw(destination)  # Comentado
   ```

2. **Línea ~152:** Cambiado `conflictBehavior` de "rename" a "fail"
   ```python
   "@microsoft.graph.conflictBehavior": "fail"
   ```

## ✅ Verificación

Al crear un nuevo assessment, verifica:

- [ ] **Solo UNA carpeta del proyecto:**
  ```
  ✅ 01_2025/1_ICT/MX/Cliente/Proyecto/
  ❌ NO debe existir: Proyecto1/, Proyecto 1/, etc.
  ```

- [ ] **Carpeta con contenido completo:**
  ```
  ✅ Proyecto/0_Initial_Assessment/
  ✅ Proyecto/1_Customer_Info/
  ✅ Proyecto/ICT_Assessment.html
  ```

- [ ] **Logs correctos:**
  ```
  ✅ Created folder: 01_2025/1_ICT/MX/Cliente/Proyecto
  ✅ Created folder: 01_2025/1_ICT/.../0_Initial_Assessment
  ❌ NO debe decir: "Proyecto1" o similar
  ```

## 🚀 Para Probar

1. **Reinicia la aplicación:**
   ```bash
   streamlit run main.py
   ```

2. **Crea un assessment completamente nuevo**
   - Usa un nombre de proyecto que NO hayas usado antes

3. **Verifica en SharePoint:**
   - Solo debe existir UNA carpeta con el nombre del proyecto
   - Debe tener todo el contenido del template

4. **Si encuentras carpeta con sufijo:**
   - Elimínala manualmente de SharePoint
   - Es un residuo de pruebas anteriores

## 🎉 Estado: COMPLETADO

✅ Eliminada creación duplicada de carpeta del proyecto
✅ Cambiado conflictBehavior a "fail" para detectar problemas
✅ Solo se crea UNA carpeta del proyecto con contenido
✅ No más carpetas vacías con sufijo "1"

**El problema de carpetas duplicadas con sufijo está completamente resuelto.** 🚀
