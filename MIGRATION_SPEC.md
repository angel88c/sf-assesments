# SPEC de Migración — iBtest Assessment Application (Streamlit → Next.js)

> Documento base generado a partir del análisis del código existente en `sf-assesments`.
> Su objetivo es capturar **qué hace la aplicación hoy** (comportamiento, integraciones y
> esquemas de datos) para servir como contrato funcional de la migración a un stack más
> robusto basado en **Next.js**.
>
> **Fecha de análisis:** Jun 2026 · **Stack actual:** Python + Streamlit 1.50 · **Stack destino:** Flask + Jinja2 + HTMX

---

## 1. Propósito del sistema

La aplicación es la **herramienta de intake de RFQ/assessments de iBtest**. Permite a
clientes externos (OEMs/EMS) y usuarios internos capturar la información técnica inicial de
un proyecto de prueba electrónica, adjuntar archivos y, con un solo envío:

1. Crear la estructura de carpetas del proyecto en el almacenamiento (SharePoint o local),
   copiando una plantilla de carpetas por BU.
2. Subir los archivos compartidos por el cliente en una subcarpeta específica.
3. Generar y guardar un **reporte HTML** del assessment dentro de la carpeta del proyecto.
4. Crear una **Oportunidad en Salesforce** (Stage "New Request") con un enlace a la carpeta
   del proyecto en SharePoint, vinculada a la Cuenta si el cliente ya existe en Salesforce.

Soporta **3 tipos de assessment** (uno por BU/servicio) — **FIX descontinuado en la migración**:

| Tipo | BU | Carpeta de proyectos | Plantilla |
|------|----|----------------------|-----------|
| **ICT** | In-Circuit Test | `1_In_Circuit Test (ICT)` | `TEMPLATE_ICT` |
| **FCT** | Functional Circuit Test | `2_Functional Test (FCT)` | `TEMPLATE_FCT` |
| **IAT** | Industrial Automation & Test | `4_Industrial Automation (IAT)` | `TEMPLATE_IAT` |
| ~~FIX~~ | ~~Fixtures~~ | ~~`7_Fixtures (FIX)`~~ | ~~sin plantilla~~ — **descontinuado en la migración** |

---

## 2. Arquitectura actual (Streamlit)

```
main.py                         # Entry point: auth check + redirect a la página destino
core/
  auth.py                       # AuthService (login email/password, sesión en st.session_state)
  exceptions.py                 # Jerarquía IBTestError (Auth, Validation, Salesforce, Storage, Config)
  logging_config.py             # Logging centralizado (dev=INFO / cloud=WARNING)
config/
  settings.py                   # Settings por dataclasses desde .env / st.secrets (singleton)
services/
  salesforce_service.py         # SalesforceService (simple-salesforce, retry con backoff)
  storage_service.py            # StorageService (abstrae el provider, crea carpetas, sube archivos, guarda HTML)
storage/
  base.py                       # StorageProvider (ABC: create_folder, folder_exists, upload_file(s), copy_template, write_file, get_full_path)
  local_storage.py              # LocalStorageProvider (sistema de archivos local)
  sharepoint_storage.py         # SharePointStorageProvider (Microsoft Graph API vía MSAL)
pages/
  ict_assessment.py             # Página ICT (secciones + main)
  fct_assessment.py             # Página FCT
  iat_assessment.py             # Página IAT
  fix_assessment.py             # Página FIX
  utils/
    base_assessment_refactored.py  # BaseAssessment: render del form + orquestación del submit
    constants.py                # Opciones fijas (YES_NO, tipos de archivo, países, opciones por BU)
    validations.py              # Validación de email corporativo + campos requeridos
    dates_info.py               # Cálculo de días hábiles / último día hábil del mes siguiente
    global_styles.py            # CSS global + logo
    auth.py                     # Decorador require_authentication
    ict_create_html.py          # Generadores de reporte HTML (uno por BU)
    fct_create_html.py
    iat_create_html.py
    fix_create_html.py
TEMPLATES/                      # Plantillas de carpetas copiadas por proyecto (TEMPLATE_ICT/FCT/IAT)
.streamlit/                     # config.toml + secrets.toml (deploy en Streamlit Cloud)
```

### Patrones clave a preservar
- **Capa de servicios** separada de la UI (`services/` + `storage/`).
- **Strategy** para storage: `StorageProvider` con dos implementaciones (local / SharePoint).
- **Singleton de configuración** tipada (`Settings`).
- **Retry con backoff exponencial** en llamadas a Salesforce.
- **Cache** de la conexión de Salesforce y de la lista de Accounts (TTL 10 min).
- **BaseAssessment** como clase común que recibe, por inyección, las secciones específicas
  de cada BU y el conversor a HTML.

---

## 3. Flujo de usuario

```
Login (email + password compartido)
   │  (autenticación contra hash SHA-256 en env)
   ▼
Página de assessment (ICT | FCT | IAT | FIX)
   ├── Sección: Información del cliente (común a todas)
   ├── Sección: Archivos a compartir (uploader + checkboxes por tipo)
   ├── Secciones técnicas (específicas por BU)
   └── Botones: Submit | Logout
         │
         ▼  (al hacer Submit)
   1. Validar datos (email corporativo, campos requeridos)
   2. Preparar datos del cliente (¿está en la lista de Salesforce? → AccountId)
   3. Crear carpeta del proyecto: {projects_folder}/{country_code}/{customer}/{project_name}/
      └ copiar la plantilla de la BU dentro
   4. Subir archivos del cliente a subcarpeta (ICT: 1_Customer_Info/7_ALL_Info_Shared
      | resto: 1_Customer_Info/3_ALL_Info_Shared)
   5. Generar HTML del assessment y guardarlo como {BU}_Assessment.html en la raíz del proyecto
   6. Crear Opportunity en Salesforce:
        Name            = project_name
        StageName        = "New Request"
        CloseDate        = último día hábil del mes siguiente
        Assessment_Date__c = hoy
        Path__c          = URL de SharePoint del proyecto
        BU__c            = assessment_type
        AccountId        = (solo si el cliente está en la lista)
   7. Mostrar resultado (éxito / error con mensajes)
```

### Reglas de negocio derivadas
- **Email corporativo obligatorio**: se rechazan dominios personales (`@gmail.com`,
  `@hotmail.com`, `@live.com.mx`, `@yahoo.com`, `@yahoo.com.mx`).
- **Fecha de cotización sugerida** = hoy + 5 días hábiles.
- **CloseDate de la Opportunity** = último día hábil (lun-vie) del mes siguiente.
- **Cliente no listado**: si el cliente no está en Salesforce, se captura el nombre en un
  campo libre (`customer_name2`) y la Opportunity se crea **sin** `AccountId`.
- **Proyecto duplicado**: si la carpeta del proyecto ya existe, se bloquea el envío con un
  error ("contacte al Sales Manager"). Hay un campo `is_duplicated?` en el form pero la
  validación real es por existencia de carpeta.
- **Tamaño máximo de upload**: 200 MB (config de Streamlit).

---

## 4. Esquema de datos — Sección común (todos los assessments)

Campos de "Información del cliente" (`BaseAssessment.create_customer_info_section`):

| Campo | Tipo | Req | Notas |
|-------|------|-----|-------|
| `project_name` | texto | * | Nombre/referencia del proyecto (→ Name de Opportunity) |
| `contact_name` | texto | * | |
| `customer_name` | select | — | Dropdown de Accounts de Salesforce (ordenado A-Z, único por nombre) + "Other" |
| `customer_name2` | texto | — | Si el cliente no está listado |
| `country` | select | — | Mexico / USA / Canada / Europe / Asia / Other → código (MX, USA, CAD, EUR, ASIA, OTHER) |
| `date` | fecha (auto) | * | Hoy (Y-m-d) |
| `quotation_required_date` | fecha | — | Default = hoy + 5 días hábiles |
| `contact_email` | texto | * | Email corporativo validado |
| `contact_phone` | texto | — | |
| `is_duplicated` | radio Yes/No | — | Default "No" |

### Archivos a compartir
- Uploader múltiple (cualquier tipo).
- Checkboxes por tipo de archivo; los marcados con `*` en la etiqueta se preseleccionan
  como obligatorios (solo UI; la validación real es de campos, no de archivos).
- El dict de tipos marcados se guarda en `info["file_types"]`.

**Tipos de archivo por BU** (`constants.py`):

- **ICT**: `*CAD files`, `*BOM`, `Gerber files`, `Schematics (pdf)`, `Test Spec (pdf, doc)`,
  `Fixture SOW`, `Board directory (.tar.gz, .tar)`
- **FCT**: `*CAD files`, `*Gerber files`, `Schematics (pdf)`, `Test Spec (pdf, doc)`,
  `BOMS`, `SOW`, `Drawings (2d, 3d)`
- **FIX**: `*CAD files`, `Gerber files`, `Schematics (pdf)`, `BOMs of each version`,
  `2D Drawings (.dwg, .dxf, .pfd, .tif)`, `3D Drawings (.step, .igs, .x_t)`,
  `Test Spec (pdf, doc)`, `Customer's SOW`, `Physical Samples`
- **IAT**: usa `IAT_MILESTONES` (lista) como "file types" — *inconsistencia a corregir*.

---

## 5. Esquemas de datos — Secciones técnicas por BU

> Conviértase cada sección en un sub-formulario React. Las opciones cerradas se listan
> literalmente para replicar los `constants.py`.

### 5.1 ICT — Secciones
1. **Feature Fixture**
   - `inline_bottom_side` (texto) — lado inferior del PCB para InLine
   - `activation_type` (radio, req): Vacuum box / Hold down gates / Pneumatic / InLine Test Fixture
     → `fixure_type` se deriva (OffLine / InLine)
   - `well_type` (radio, req): Single well / Dual well / Dual stage
   - `size_type` (radio, req): Small Kit / Large Kit / Small Extended / Large Extended
   - `fixture_vendor` (texto): Circuit Check, Rematek, Arcadia, Juarez Technology, QxQ...
   - `versions` (número, min 1)
2. **Flash Programming** (expander)
   - `flash_programming` (radio: NA / Required / Optional)
   - `programmer_brand` (texto): FlashRunner 2.0, FRCube, Phyton, Algocraft, Segger...
   - `program_devices` (texto → lista por coma): TC387, PIC16F628... → `quantity_devices`
   - `logistic_data` (Yes/No)
   - `items_for_logistic_data` (texto)
3. **Test Specifications**
   - `test_spec`, `fixture_sow`, `config_file` (Yes/No)
4. **Panel**
   - `panel_test`, `individual_test` (Yes/No)
   - `quantity_panel`, `quantity_nest` (número, min 1)
5. **Additional Requirements**
   - `automatic_scanner` (NA/Required/Optional), `scanner_brand`
   - `board_presence` (NA/Required/Optional)
   - `window_and_holder`, `switch_probe_on_connector`, `custom_tests`, `color_test` (Yes/No)
   - `custom_tests_info`, `color_test_info` (texto)
   - `clock_module` (NA/Required/Optional)
   - `testjet` (NA/Required/Optional), `ics_with_testjet`
   - **Boundary Scan** (expander): `boundary_scan`, `silicon_nails` (NA/Required/Optional),
     `required_ics`
6. **Additional Information** (común): `travel`, `entity_po`, `additional_comments`

### 5.2 FCT — Secciones
1. **Milestones**
   - `cad_files`, `gerber_files`, `schematics`, `boms`, `traceability_system`, `sow`,
     `drawings`, `test_spec`, `parallel_testing`, `security_specification` (Yes/No)
   - `osp_finish` (Yes/No, default No)
   - `product_finish` (select): PCB / Assembly
   - `test_strategy` (select): Panel / Depanelized
   - `connection_interface` (select): MACPANEL / INGUN / VPC / Harting / iBtest suggestion / Other
   - `traceability_system_name` (texto): ITAC, MES...
   - `ergonomy_specifications` (texto)
   - `quantity_uut` (número, req, min 1)
   - `fixture_vendor` (select): iBtest / CCI / Rematek / JT / Arcadia / Joule / Other
2. **FCT System Assessment**
   - `studies_necessaries` (multiselect): FEA / SGA / MSA / GRR / R&R / Targeting / Clearance
   - `qty_microstrains` (texto)
   - `hardware_option` (select): NI / Keysight / BK / Chroma / GW
   - `system_type` (select, req): Flexicore / Venturi / Viper / SLU / ECUTS / iBFlash / None
   - `station_type` (select, req): EOL / Flash / FVT / HIPOT / Vision / Communication / Chamber / Other
   - `process_type` (select, req): Offline / Inline / Rotaty / Automated Process
   - `scanner_brand` (select): Keyence / Cognex / Microscan / Other
   - `rosettes` (texto)
   - `fixture_needs` (área de texto)
   - `dm_position` (área de texto)
   - `modifications_customer` (Yes/No, default No)
   - `test_sequencer` (select, req): LabView / TestStand / CVI / TestExec / Other
3. **Testing System Specifications**
   - `dimensions`, `test_execution_conditions` (Yes/No, default No)
   - `dimensions_spec`, `test_execution_conditions_spec` (texto)
4. **Product and Testing System Requirements**
   - `single_product`, `self_test_required`, `certification_required` (Yes/No, default No)
   - `single_product_info`, `self_test_required_info`, `certification_required_info` (texto)
   - `certifications_option` (select): CE / EMV / VDE / Calibration / UL / Other
5. **Additional Information** (común)

### 5.3 IAT — Secciones
1. **Milestones** (cada uno Yes/No, con sub-campos de texto asociados)
   - `cad_files`, `process_spec`, `nests` (+ `qty_nests`),
     `plc_programming_standard`, `sow_ergonomic_spec`, `layout` (+ `dimensions`),
     `product_manufacturing_sheet`, `traceability` (+ `traceability_name`),
     `estimated_cycle_time` (+ `cycle_time`), `special_handling` (+ `special_handling_info`),
     `customer_has_samples`
2. **Station Features**
   - `station_type` (select, req): Refurbish / Engineering Service / Equipment Modification /
     Cell / Stand Alone / Add New Model / Other
   - `station_type_info` (área de texto)
   - `process_type` (select, req): Testing / AOI / Assembly / Screwing Station / Dispensing Machine / Other
   - `process_type_info` (área de texto)
   - `uut_handle_mode` (select, req): Magazine / Human / Robot or Cobot / Axis System /
     Conveyor / Automatic / Manual / Other
   - `uut_handle_mode_info` (área de texto)
   - `device_under_process` (select): Housing / PCB / Other
   - `design_required` (Yes/No) + `design_required_info`
   - `certifications_required` (Yes/No) + `certifications_info`
   - `preferent_hardware` (área de texto)
   - `acceptance_criteria` (área de texto)
   - `general_info_requirement` (área de texto)
3. **Additional Information** (común)

### 5.4 FIX — Secciones
1. **General Product Information**
   - `product_use_type` (radio): Single Product / Multiple Products + comments
   - `test_type` (select): ICT / Flashing / Functional Test / LED Test / Hi-Pot / RF Test + comments
   - `dut_assembly_level` (select): Housing / PCBA / Other + comments
   - Bloque milestones (con status Yes/No + Qty + Comments): `Panel Test?`,
     `Individual Test?`, `Is the product NPI or design freeze?`
   - `purpose_fixture` (select): Off-line / In-Line / Conveyor Pallet + comments
   - `pcb_side`, `products_manufacture` (texto)
   - `activation_type` / `well_type` / `size_type` / `fixture_vendor` / `versions`
     (mismos que ICT)
2. **Fixture Configuration**
   - **Connectivity to the DUT** (checkbox + comments por cada uno): Test Points,
     Connectors, Through hole, Wire Harness, RF Coaxial, Other
   - Bloque milestones con status/qty/comments: Mass Interconnect System, Harness
     connectors, Special connectors on fixture's back, Bottom nodes to access, Top nodes to
     access, Side access connections, Specify the type of socket's tail, Door closed lock,
     Automatic Opening, Counter, Product presence sensor, BoardMarkes, Scanner, LED Test,
     Instalation of special hardware, Does the fixture need internal wiring labor?, FEA
     Study?, Strain gage study?
3. **Additional Information** (común)

> **Patrón recurrente FIX**: existe un generador `generate_milestones(item, milestones)`
> que renderiza filas con **Status (Yes/No) + Qty (número) + Comments (texto)**. Este patrón
> debe modelarse como una sub-estructura de datos repetible en el nuevo stack.

---

## 6. Integraciones

### 6.1 Salesforce (`simple-salesforce`, OAuth username/password + security token)
- **Autenticación**: username + password + security_token + consumer_key/secret (connected app).
- **`get_accounts()`** → `SELECT Id, Name FROM Account ORDER BY Name ASC`, de-duplica por
  nombre, agrega "Other", cachea 10 min. Alimenta el dropdown de cliente.
- **`create_opportunity()`** crea registro `Opportunity` con campos:
  `Name`, `StageName` ("New Request"), `CloseDate`, `Assessment_Date__c` (custom),
  `Path__c` (custom), `BU__c` (custom), `AccountId?`.
- **Resiliencia**: decorador `retry_on_timeout` (max 3 reintentos, backoff exponencial
  base 2s, tope 30s) sobre `Timeout`/`ConnectionError`.
- **Mapeo a Flask**: **reutilizar `simple-salesforce` tal cual** (ya probado con tus
  campos custom). Quitar decoradores `@st.cache_*` y usar `functools.lru_cache` o caché
  propio con TTL. Credenciales server-side, nunca expuestas al cliente.

### 6.2 SharePoint (Microsoft Graph API vía MSAL, client-credentials)
- **Auth**: `ConfidentialClientApplication` con tenant_id/client_id/client_secret,
  scope `https://graph.microsoft.com/.default`.
- **Operaciones**: `create_folder`, `folder_exists`, `upload_file` (upload simple <4MB;
  *falta upload resumible para >4MB*), `upload_files`, `copy_template` (recorre el árbol
  local con `rglob` y crea carpetas/sube archivos uno a uno), `write_file` (HTML report).
- **Config**: `site_id`, `drive_id`, `base_path` (ej. `01_2025`).
- **Endpoint Graph**: `https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{path}`.
- **Mapeo a Flask**: **reutilizar `storage/sharepoint_storage.py` tal cual** (MSAL +
  requests). Todo server-side, el token de Graph nunca llega al browser. Considerar
  chunks/sesiones de upload resumible para archivos grandes (hasta 200MB) — Fase 3.

### 6.3 Almacenamiento local (alternativa/dev)
- `LocalStorageProvider` opera sobre el filesystem (`PATH_FILE`). Mantiene la misma interfaz
  `StorageProvider`. Útil para entorno de desarrollo.

---

## 7. Estructura de carpetas por proyecto (output del submit)

```
{base_path}/                                              # raíz SharePoint (base_path ej: 01_2025)
└── {projects_folder}/                                    # ej: 1_In_Circuit Test (ICT)
    └── {country_code}/                                   # MX | USA | CAD | EUR | ASIA | OTHER
        └── {customer_name}/
            └── {project_name}/                           # raíz del proyecto (creada + plantilla copiada)
                ├── ICT_Assessment.html                   # reporte generado (uno por BU)
                ├── 0_Initial Assessment/
                ├── 1_Customer_Info/
                │   ├── 1_CAD_Files/ ... (estructura de plantilla)
                │   └── 7_ALL_Info_Shared/  ← archivos del cliente (ICT)
                │       (3_ALL_Info_Shared para FCT/IAT/FIX)
                ├── 2_Supplier_Quotes/
                ├── 3_Fixture_RFQ_&_Testsight_Files/      # (varía por plantilla)
                └── 4_iBTest_Quotation/
```

- **Validación de duplicidad**: si `{project_name}` ya existe → error (bloquea envío).
- **URL de SharePoint** guardada en `Opportunity.Path__c` =
  `{PATH_TO_SHAREPOINT}/{project_relative_path}`.

---

## 8. Modelo de autenticación (actual y recomendado)

### Actual
- **Una sola credencial compartida** (email + password) para todos los usuarios.
- Password hasheado **SHA-256 sin salt** (débil) almacenado en env/secrets.
- Sesión en `st.session_state` (efímera, por pestaña).
- Decorador `require_authentication` por página; logout redirige a `main.py`.

### Decidido para Flask (híbrido SSO + cuentas locales)
- **Flask-Login + authlib** con dos providers:
  1. **Azure AD (Microsoft SSO)** vía `authlib` (OAuth2) — para usuarios internos y clientes
     con cuenta M365 (alineado al stack iBtest, IdP corporativo).
  2. **Credenciales locales** en PostgreSQL — para usuarios externos **sin** cuenta
     Microsoft (clientes/prospectos). Permite invitar usuarios externos en el futuro sin
     depender de M365. Flask-Login gestiona la sesión.
- Cuentas locales: bcrypt/argon2 (nunca SHA-256 plano), tabla `users` en PostgreSQL.
- Sesión vía cookie firmada de Flask; **nunca** exponer tokens al cliente.
- Modela roles: `internal` (SSO) vs `external` (cuenta local) para reglas de acceso futuro.

---

## 9. Requisitos no funcionales (a preservar/mejorar)

| Área | Actual | Migración |
|------|--------|-----------|
| **Caché de Accounts** | `st.cache_data` TTL 10 min | `functools.lru_cache` con TTL o caché server-side simple |
| **Caché de conexiones** | `st.cache_resource` | Singleton a nivel módulo (patrón ya existente en `get_settings()`) |
| **Reintentos SF** | backoff exponencial 2→30s, max 3 | **Reutilizar** `retry_on_timeout` decorador actual |
| **Upload máx** | 200 MB | Confirmar; usar upload resumible (Graph: createUploadSession) — Fase 3 |
| **Logging** | INFO/WARNING según entorno | **Reutilizar** `core/logging_config.py` |
| **Validación email** | blocklist de dominios personales | **Reutilizar** `validations.py` |
| **Fechas hábiles** | cálculo en `dates_info.py` | **Reutilizar** `dates_info.py` (lun-vie, sin festivos) |
| **i18n** | inglés hardcoded | ES/EN desde inicio con **Flask-Babel** — clientes MX y USA |
| **Disponibilidad** | Streamlit Cloud / cloudflared on-prem | **Easypanel sobre VPS** (PaaS con Docker, gunicorn + nginx). |

---

## 10. Arquitectura destino sugerida (Flask + Jinja2 + HTMX)

```
sf-assessments/                                # refactor del proyecto actual
├── app/                                       # Flask application factory + blueprints
│   ├── __init__.py                            # create_app()
│   ├── config.py                              # Flask config (reutiliza config/settings.py)
│   ├── auth/
│   │   ├── __init__.py                        # blueprint auth_bp
│   │   ├── routes.py                          # /login, /logout, /auth/azure/callback
│   │   ├── azure_ad.py                        # OAuth2 con authlib (Azure AD)
│   │   └── decorators.py                      # @login_required (reemplaza require_authentication)
│   ├── assessments/
│   │   ├── __init__.py                        # blueprint assessments_bp
│   │   ├── routes.py                          # GET /assessments/ict, POST /assessments/ict/submit
│   │   ├── forms.py                           # WTForms por BU (ICT/FCT/IAT)
│   │   ├── orchestrator.py                    # process_submission() (de BaseAssessment, sin st.*)
│   │   └── html_report.py                     # render_report() con Jinja2
│   ├── api/
│   │   ├── __init__.py                        # blueprint api_bp (endpoints HTMX/JSON)
│   │   └── accounts.py                        # GET /api/accounts (HTMX partial / JSON)
│   ├── models/
│   │   ├── __init__.py                        # SQLAlchemy db instance
│   │   ├── user.py                            # User, LocalUser (cuentas locales + SSO)
│   │   └── submission.py                      # SubmissionsAudit
│   ├── templates/
│   │   ├── base.html                          # layout: logo, nav, logout, bloques i18n
│   │   ├── auth/login.html
│   │   ├── assessments/
│   │   │   ├── _macros_common.html            # macros: customer_info, files, additional_info
│   │   │   ├── ict/form.html
│   │   │   ├── ict/_sections.html             # feature_fixture, flash, test_spec, panel, additional_req
│   │   │   ├── fct/...
│   │   │   └── iat/...
│   │   └── reports/
│   │       └── ict_report.html                # template del HTML report (reemplaza f-strings)
│   └── static/
│       ├── css/                               # Tailwind (build) o CSS
│       ├── js/                                # htmx.min.js, alpine.min.js (opcional)
│       └── img/logo_ibtest.png
├── services/                                  # ★ REUTILIZADO del proyecto actual
│   ├── salesforce_service.py                  # (quitar @st.cache_*, usar lru_cache con TTL)
│   └── storage_service.py                     # (quitar @st.cache_resource)
├── storage/                                   # ★ REUTILIZADO sin cambios
│   ├── base.py
│   ├── local_storage.py
│   └── sharepoint_storage.py
├── core/                                      # ★ REUTILIZADO sin cambios
│   ├── exceptions.py
│   └── logging_config.py
├── config/                                    # ★ REUTILIZADO (quitar refs a st.secrets)
│   └── settings.py
├── utils/                                     # ★ REUTILIZADO de pages/utils/
│   ├── constants.py                           # (de pages/utils/constants.py)
│   ├── dates_info.py                          # (de pages/utils/)
│   └── validators.py                          # (de pages/utils/validations.py)
├── migrations/                                # Alembic (SQLAlchemy)
├── TEMPLATES/                                 # plantillas de carpetas (sin cambios)
├── tests/
├── requirements.txt                           # Flask + deps (ver stack)
├── Dockerfile                                 # para Easypanel
└── .env
```

### Mapeo de responsabilidades
| Streamlit actual | Flask destino |
|------------------|---------------|
| `main.py` + `require_authentication` | `@login_required` (Flask-Login) + blueprint protegido |
| `BaseAssessment.render_form` | Templates Jinja2 + WTForms (forms.py) |
| `BaseAssessment.process_form_submission` | `assessments/orchestrator.py` (lógica sin `st.*`) |
| `services/salesforce_service.py` | **Reutilizado** (quitar `@st.cache_*`) |
| `storage/*` (Strategy) | **Reutilizado** sin cambios |
| `pages/utils/*_create_html.py` (f-strings) | `templates/reports/*.html` (Jinja2, casi 1:1) |
| `config/settings.py` | **Reutilizado** (quitar refs a `st.secrets`, solo dotenv) |
| `core/exceptions.py`, `logging_config.py` | **Reutilizados** sin cambios |
| `pages/utils/constants.py` | `utils/constants.py` (mover, sin cambios) |
| `pages/utils/dates_info.py` | `utils/dates_info.py` (mover, sin cambios) |
| `pages/utils/validations.py` | `utils/validators.py` (mover, sin cambios) |
| *(nuevo)* | `app/models/` (SQLAlchemy) — usuarios locales + auditoría |

### Stack recomendado
- **Framework**: Flask + Jinja2 (backend + templates server-rendered, una sola app)
- **Interactividad**: HTMX (AJAX declarativo sin SPA) + Alpine.js opcional para micro-estado
- **Tablas de datos**: **AG Grid Community** como estándar UI — filtros y paginación
  habilitados por defecto en toda tabla. Vistas previstas (Fase 2/3): historial de
  `submissions_audit`.
- **UI/CSS**: Tailwind CSS (mantiene el look actual de los reportes HTML)
- **Formularios**: Flask-WTF (WTForms) — validación server-side + CSRF
- **Auth**: Flask-Login (sesión) + authlib (OAuth2 Azure AD) + bcrypt (cuentas locales)
- **DB**: PostgreSQL + SQLAlchemy + Alembic (migraciones)
- **Salesforce**: **`simple-salesforce` reutilizado** (con `retry_on_timeout` actual)
- **SharePoint**: **MSAL + requests reutilizados** (`storage/sharepoint_storage.py`)
- **Reportes HTML**: Jinja2 templates (`render_template_string` o `render_template` a archivo)
- **i18n**: Flask-Babel (ES/EN)
- **Caché**: `functools.lru_cache` con TTL casero o `cachetools` (sin Redis en Fase 1)
- **Hosting**: Easypanel sobre VPS (Docker, gunicorn + nginx, SSL gestionado)
- **Observabilidad**: `core/logging_config.py` reutilizado + Sentry opcional

### Por qué este stack para este proyecto
1. **Reutiliza ~70% del backend Python intacto** (services, storage, config, core, utils).
2. **Una sola app en producción** — un Docker, un deploy, menos piezas operativas para
   equipo de 4.
3. **Cero riesgo de reescritura de integraciones** (simple-salesforce y MSAL ya probados
   con campos custom `BU__c`, `Path__c`).
4. HTMX da interactividad suficiente para forms (validación, collapsibles, toasts) sin
   construir una SPA pesada.
5. Curva de aprendizaje mínima para el equipo (ya son Python).

### 10.1 Identidad visual — Paleta corporativa (Teal + DarkBlue + WhiteSmoke)

La nueva UI reemplaza los estilos genéricos de Streamlit por una paleta corporativa
consistente, aplicada tanto en la app como en los reportes HTML generados (para que el
archivo `ICT_Assessment.html` que ve el cliente tenga la misma identidad).

**Paleta base**

| Token | Hex | Uso |
|-------|-----|-----|
| `--dark-blue` | `#16337D` | Color primario de marca. Botones, headers, títulos, enlaces, logo primario. *(ya usado en `global_styles.py`)* |
| `--dark-blue-hover` | `#00072D` | Hover/active de botones. *(ya usado)* |
| `--teal` | `#0D9488` | Color secundario/acento. Botones secundarios, badges, selects foco, bordes de sección, links de acción. |
| `--teal-light` | `#F0FAF9` | Fondo general de la app (muy claro). *(ya usado como fondo en Streamlit)* |
| `--teal-tint` | `#E6F4F3` | Fondo de tarjetas/secciones alternas, hover de filas. |
| `--whitesmoke` | `#F5F5F5` | Fondo neutro de inputs, áreas de carga, separadores. |
| `--ink` | `#1F2937` | Texto principal (gray-800). |
| `--muted` | `#4B5563` | Texto secundario/labels (gray-600). |
| `--border` | `#E5E7EB` | Bordes y divisores (gray-200). |
| `--danger` | `#DC2626` | Errores / validación. |
| `--success` | `#16A34A` | Éxito (toast verde). |

**Reglas de uso**
- **Fondo general** = `--teal-light` (`#F0FAF9`). Las tarjetas/formularios sobre blanco
  con sombra suave (mantiene el look actual de `st.container(border=True)`).
- **Botón primario** (Submit) = `--dark-blue` con texto blanco; hover `--dark-blue-hover`.
- **Botón secundario** (Logout, acciones menores) = outline `--teal` / texto `--teal`.
- **Inputs/selects** foco = borde `--teal` (`--tw-ring-color`).
- **Títulos de sección** (`subtitle_h3`) = `--dark-blue`; subtítulos `subtitle_h4` = `--muted`.
- **Acentos** (badges BU, asterisco de requerido, separadores de tarjeta) = `--teal`.
- **Reportes HTML** (`*_report.html`): la misma paleta vía Tailwind (clases arbitrarias
  `bg-[#16337D]` o tokens de `tailwind.config`). Garantiza que el archivo que recibe el
  cliente tenga identidad iBtest al abrirlo en el navegador.

**Implementación con Tailwind**
Configurar `tailwind.config.js` con los tokens como colores custom para usar clases
semánticas (`bg-brand`, `text-brand`, `bg-teal-light`, etc.) en toda la app y reportes:

```js
// tailwind.config.js (extracto)
theme: {
  extend: {
    colors: {
      brand: { DEFAULT: "#16337D", hover: "#00072D" },     // DarkBlue
      teal:  { DEFAULT: "#0D9488", light: "#F0FAF9", tint: "#E6F4F3" },
      smoke: "#F5F5F5",                                    // WhiteSmoke
      ink: "#1F2937", muted: "#4B5563",
      border: "#E5E7EB",
    },
    fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] }, // Inter ya en reportes actuales
    boxShadow: { card: "0px 4px 10px rgba(0,0,0,0.08)" },
    borderRadius: { card: "15px", field: "8px" },
  },
}
```

> El logo `logo_ibtest.png` ya existe en el repo y se mantiene. Fuentes: **Inter**
> (ya referenciada en `ict_create_html.py` vía Google Fonts) como tipografía base.

### 10.2 Estándar de tablas — AG Grid Community

Cualquier tabla de datos en la app usa **AG Grid Community (MIT)** con configuración
consistente. Integración con Flask: AG Grid es JS puro, se inicializa sobre un
`<div id="grid">` con datos servidos como JSON (endpoint Flask o atributo `data-*`).

**Configuración por defecto** (aplicar a toda tabla vía helper/wrapper):

| Opción | Valor | Notas |
|--------|-------|-------|
| `pagination` | `true` | Paginación habilitada |
| `paginationPageSize` | `25` | Tamaño de página base |
| `paginationPageSizeSelector` | `[10, 25, 50, 100]` | Selector de tamaño |
| `defaultColDef.filter` | `true` | Filtro habilitado en **todas** las columnas |
| `defaultColDef.floatingFilter` | `true` | Fila de filtros siempre visible debajo del header |
| `defaultColDef.sortable` | `true` | Sort por columna |
| `defaultColDef.resizable` | `true` | Redimensionar columnas |
| `defaultColDef.flex` | `1` | Distribución responsive del ancho |
| `rowSelection` | (según vista) | `multiple` en admin, `none` en historial read-only |
| `animateRows` | `true` | Animación de filas al sort/filtro |
| `domLayout` | `autoHeight` | Evita scroll interno cuando hay pocas filas |

**Tematización con la paleta corporativa** (§10.1):

```js
const gridOptions = {
  // ...opciones de arriba
  rowClassRules: {
    "bg-teal-tint": (params) => params.node.rowIndex % 2 === 1, // filas alternas
  },
  headerClass: "bg-brand text-white",        // header DarkBlue
  headerHeight: 40,
  rowHeight: 38,
  // Paginación UI
  paginationNumberFormat: (params) => `[${params.value}]`,
};
```

Quasar-style CSS override (en `static/css/ag-grid-ibtest.css`) para alinear el tema
por defecto de AG Grid con la paleta iBtest:
- Header background `--dark-blue`, texto blanco.
- Filas alternas `--teal-tint` / blanco.
- Borde de celda `--border`.
- Foco de filtro `--teal`.
- Botones de paginación en `--dark-blue`.

**Vistas previstas (alcance por fase)**

| Vista | Datos | Fase | Rol |
|-------|-------|------|-----|
| **Historial de submissions** | `submissions_audit`: fecha, usuario, BU, proyecto, estado (success/failed), `opportunity_id`, `error_code`, `duration_ms` | **Fase 2/3** | `internal` (iBtest) |
| *(futuro)* Cuentas locales | `users`: email, rol, estado, fecha creación | Fase 3 (admin) | `internal` admin |
| *(futuro)* Accounts Salesforce | cache de `getAccounts()`: nombre, ID | Fase 3 (admin) | `internal` admin |

**Endpoint de datos** (patrón):
- Flask route `GET /api/submissions` (JSON, con query params `page`, `pageSize`, filtros).
- Server-side: paginación/filtro opcionales en SQL (SQLAlchemy) para datasets grandes;
  client-side si <1000 filas (carga completa al grid). Empezar con client-side (más simple).

**Wrapper para evitar repetición**:
```js
// static/js/ibtest-grid.js
export function createIbtestGrid(divId, columnDefs, rowData, opts = {}) {
  return new agGrid.Grid(document.getElementById(divId), {
    gridOptions: {
      ...IBTEST_DEFAULT_GRID_OPTIONS,  // la config de arriba
      columnDefs,
      rowData,
      ...opts,                          // override por vista
    }
  }).gridOptions;
}
```

> **Fase 1**: el estándar se documenta aquí pero **no se implementa** (la Fase 1 es el
> vertical slice ICT: form + submit + auditoría escrita). La vista de historial con AG
> Grid se construye en Fase 2/3 cuando hay datos que mostrar.

---

## 11. Deuda técnica / bugs detectados (a resolver en la migración)

1. **`Path` no importado** en `base_assessment_refactored.py:279` (`_get_sharepoint_url`):
   rompería en runtime al construir la URL de SharePoint.
2. **FIX mal tipado**: `fix_assessment.py:186` crea el `BaseAssessment` con
   `assessment_type="IAT"` (debería ser `"FIX"`), y `projects_folder` apunta a
   `7_Fixtures (FIX)` pero **no existe `TEMPLATE_FIX`** (solo ICT/FCT/IAT). La oportunidad
   en Salesforce se crearía con `BU__c = "IAT"`. **Decidir:** crear plantilla FIX o unificar.
3. **IAT pasa `file_types=IAT_MILESTONES`** (una lista) en lugar de un dict como ICT/FCT/FIX;
   el `upload_files` de `BaseAssessment` espera un dict iterable de tipos. Inconsistencia.
4. **Auth débil**: SHA-256 sin salt + credencial única compartida (ver §8).
5. **Upload de SharePoint sin sesión resumible**: archivos >4MB no se manejan correctamente
   (el código usa el endpoint simple `/content`). El límite de 200MB del form no se cumple
   en el provider de SharePoint.
6. **Validaciones incompletas**: `validate_fields` solo valida 4 campos comunes; no valida
   los campos técnicos marcados con `*` en cada BU, ni los archivos obligatorios.
7. **README con conflicto Git sin resolver** (`<<<<<<< HEAD` ... `>>>>>>>`) — limpiar.
8. **`copy_template` de SharePoint** sube archivo por archivo y crea carpetas una a una:
   lento y propenso a dejar estructuras a medias si falla a la mitad. Considerar
   transaccionalidad/rollback.
9. **Códigos de país** inconsistentes: `Canada → "CAD"` (debería ser `CA`), `Europe`/`Asia`
   como "países" con códigos `EUR`/`ASIA`.

---

## 12. Alcance del MVP de migración (propuesta)

> **Decisión de scope**: FIX se **descontinúa**. La migración cubre ICT, FCT e IAT.

**Fase 0 — Fundaciones**
- Scaffold Next.js (App Router) + TS + Tailwind + shadcn/ui.
- Config tipada (zod) + env.
- Auth.js: provider Azure AD (SSO) + Credentials con cuentas locales en PostgreSQL.
- PostgreSQL + ORM (Prisma/Drizzle): tablas `users` (locales) y `submissions_audit`.
- `next-intl` ES/EN (catálogos + routing locale).
- Layout protegido + login + logout.
- Deploy en Easypanel (VPS) con Docker.

**Fase 1 — ICT end-to-end (vertical slice)**
- Form ICT completo con Zod (secciones comunes + técnicas), mensajes ES/EN.
- BFF: `GET /api/accounts` (cacheado, jsforce) y `POST /api/assessments`.
- Storage Strategy (local + SharePoint) + copia de plantilla ICT.
- Generación de reporte HTML ICT vía `react-dom/server`.
- Creación de Opportunity en Salesforce (jsforce) con retry/backoff.
- Auditoría de cada intento (payload + resultado) en `submissions_audit`.
- Validar el flujo completo contra entorno de pruebas.

**Fase 2 — FCT + IAT**
- Replicar el patrón de ICT para FCT e IAT (reusar secciones comunes).
- Corregir el bug de IAT (`file_types=IAT_MILESTONES` → dict consistente).

**Fase 3 — Robustez**
- Upload resumible para SharePoint (>4MB y hasta 200MB).
- Reintentos/circuit breaker en Salesforce y Graph.
- Observabilidad y manejo transaccional del submit (carpeta + archivos + HTML + Opportunity + auditoría).
- Panel/admin mínimo para gestionar cuentas locales externas.

---

## 13. Decisiones resueltas

| # | Decisión | Elección |
|---|----------|----------|
| 1 | **Autenticación** | Microsoft SSO (Azure AD) **+ cuentas locales** en PostgreSQL para usuarios externos sin cuenta Microsoft. Auth.js con dos providers. |
| 2 | **Hosting** | **Easypanel sobre VPS** (PaaS con Docker, SSL y dominios gestionados). |
| 3 | **Cliente Salesforce** | **Node + jsforce** dentro del BFF de Next.js (un solo stack). |
| 4 | **Reportes HTML** | **Server-render React→HTML** (`react-dom/server` `renderToString`). |
| 5 | **Assessment FIX** | **Descontinuar**. La migración cubre ICT, FCT e IAT. |
| 6 | **Base de datos** | **PostgreSQL** (Prisma/Drizzle) para usuarios locales + auditoría de submissions. No reemplaza Salesforce/SharePoint. |
| 7 | **i18n** | **ES/EN desde inicio** con `next-intl`. |
| 8 | **Calendario festivo** | **Solo días hábiles lun-vie** (sin festivos), igual que el comportamiento actual. |
| 9 | **Identidad visual** | Paleta corporativa **Teal + DarkBlue + WhiteSmoke** (`#0D9488` / `#16337D` / `#F5F5F5`) con Tailwind. Misma identidad en la app y en los reportes HTML generados. |
| 10 | **Tablas de datos** | **AG Grid Community** como estándar UI con filtros + paginación por defecto. Vista de historial de `submissions_audit` en Fase 2/3 (no en Fase 1). |

---

*Especificación base para la migración. Siguiente paso sugerido: refinar el MVP de la Fase 1
(ICT) a un plan de ejecución detallado a partir de las decisiones resueltas en la sección 13.*
