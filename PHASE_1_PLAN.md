# Plan de Ejecución — Fase 1: ICT Vertical Slice

> Plan ejecutable detallado para el primer vertical slice de la migración
> (Streamlit → **Flask + Jinja2 + HTMX**). Cubre el assessment **ICT end-to-end**.
>
> **Prerrequisito**: la Fase 0 (fundaciones) se asume **ya completada**:
> scaffold Flask + application factory; Flask-Login + authlib (Azure AD + cuentas locales);
> SQLAlchemy + Alembic + PostgreSQL; Flask-Babel ES/EN; Tailwind configurado con la paleta
> corporativa (Teal + DarkBlue + WhiteSmoke, ver `MIGRATION_SPEC.md` §10.1); deploy en
> Easypanel (VPS) con Docker; `base.html` + login/logout funcional.
>
> **Documentos base**: `MIGRATION_SPEC.md` (funcionalidad, esquemas, decisiones),
> `PALETTE_PREVIEW.html` (referencia visual).
> **Sin estimaciones de esfuerzo** — el equipo las asigna después.

---

## 1. Objetivo de la Fase 1

Entregar el flujo **completo y verificable** del assessment ICT, replicando el
comportamiento actual de `pages/ict_assessment.py` + `BaseAssessment` pero en Flask:

> Un usuario autenticado completa el form ICT → al submit: se valida, se crea la carpeta
> del proyecto con plantilla, se suben archivos, se genera el HTML, se crea la Opportunity
> en Salesforce, se audita el intento y se muestra el resultado.

### Entregables
1. Form ICT funcional (ES/EN) con validación server-side (Flask-WTF) + CSRF.
2. Rutas: `GET /assessments/ict` (render form) y `POST /assessments/ict/submit`
   (orquestador); `GET /api/accounts` (HTMX partial / JSON, cacheado).
3. Servicios reutilizados: `services/salesforce_service.py`, `services/storage_service.py`,
   `storage/*` (Strategy local/sharepoint) — quitando refs a `st.*`.
4. Orquestador `app/assessments/orchestrator.py` (lógica de `BaseAssessment` sin `st.*`).
5. Generador de reporte HTML ICT con Jinja2 (`templates/reports/ict_report.html`).
6. Modelo `SubmissionsAudit` en SQLAlchemy + escritura en cada intento.
7. UI con paleta corporativa (Tailwind tokens `brand`/`teal`/`smoke`) + HTMX para toasts.
8. Flujo E2E verificado contra entorno de pruebas (SF sandbox + SharePoint test).

### Fuera de alcance (Fase 2/3)
- FCT, IAT (Fase 2); FIX descontinuado.
- AG Grid / historial de submissions (Fase 2/3).
- Upload resumible >4MB (Fase 3).
- Circuit breaker, reintentos avanzados en Graph.
- Panel admin de cuentas locales.

---

## 2. Arquitectura de la Fase 1

Estructura de archivos a crear/mover (los marcados ★ se **reutilizan** del proyecto actual):

```
sf-assessments/
├── app/                                       # nuevo — aplicación Flask
│   ├── __init__.py                            # create_app() factory
│   ├── config.py                              # config Flask (envía a config/settings.py)
│   ├── auth/                                  # (de Fase 0)
│   ├── assessments/
│   │   ├── __init__.py                        # blueprint assessments_bp
│   │   ├── routes.py                          # GET /assessments/ict, POST .../submit
│   │   ├── forms.py                           # WTForms: IctForm + secciones
│   │   ├── orchestrator.py                    # process_submission() — de BaseAssessment sin st.*
│   │   └── report.py                          # render_ict_report(payload) -> str HTML
│   ├── api/
│   │   ├── __init__.py                        # blueprint api_bp
│   │   └── accounts.py                        # GET /api/accounts (HTMX/JSON, cacheado)
│   ├── models/
│   │   ├── __init__.py                        # db = SQLAlchemy()
│   │   ├── user.py                            # (de Fase 0)
│   │   └── submission.py                      # SubmissionsAudit (nuevo)
│   ├── templates/
│   │   ├── base.html                          # (de Fase 0) layout + logo + nav + logout
│   │   ├── assessments/
│   │   │   ├── _macros_common.html            # macros: customer_info, files, additional_info
│   │   │   ├── ict/
│   │   │   │   ├── form.html                  # página ICT
│   │   │   │   ├── _sections.html             # feature_fixture, flash, test_spec, panel, additional_req
│   │   │   │   └── _success.html              # partial HTMX tras submit exitoso (toast + link)
│   │   │   └── _error.html                    # partial HTMX de error (toast por error_code)
│   │   └── reports/
│   │       └── ict_report.html                # template del HTML report (reemplaza f-strings)
│   └── static/
│       ├── css/tailwind.css                   # build de Tailwind (tokens §10.1)
│       ├── js/
│       │   ├── htmx.min.js                    # (de Fase 0)
│       │   └── assessments.js                 # helpers: split por coma de program_devices, etc.
│       └── img/logo_ibtest.png                # (mover de raíz)
├── services/                                  # ★ REUTILIZADO (quitar @st.cache_*)
│   ├── salesforce_service.py
│   └── storage_service.py
├── storage/                                   # ★ REUTILIZADO sin cambios
│   ├── base.py
│   ├── local_storage.py
│   └── sharepoint_storage.py
├── core/                                      # ★ REUTILIZADO sin cambios
│   ├── exceptions.py
│   └── logging_config.py
├── config/                                    # ★ REUTILIZADO (quitar refs a st.secrets)
│   └── settings.py
├── utils/                                     # ★ REUTILIZADO (mover de pages/utils/)
│   ├── constants.py                           # YES_NO, ACTIVATION_TYPES, ICT_FILE_TYPES, ...
│   ├── dates_info.py                          # addWorkingDays, lastWeekdayOfNextMonth
│   └── validators.py                          # isCorporateEmail, validate_required_fields
├── TEMPLATES/                                 # plantillas de carpetas (sin cambios)
├── tests/
│   ├── conftest.py                            # fixtures: app, client, mock SF/SP
│   ├── test_orchestrator_ict.py
│   ├── test_api_accounts.py
│   ├── test_api_submit_ict.py
│   ├── test_forms_ict.py
│   └── test_report_ict.py
├── migrations/                                # Alembic (de Fase 0 + nueva tabla)
├── requirements.txt                           # Flask + deps (ver §11)
├── Dockerfile                                 # para Easypanel (de Fase 0)
└── .env
```

### Convenciones
- **Reutilización**: todo bajo `services/`, `storage/`, `core/`, `config/`, `utils/`
  viene del proyecto actual; solo se **quitan las refs a `st.*`** (`@st.cache_*`,
  `st.session_state`, `st.secrets`).
- **Server-side**: todo el procesamiento es backend Python; los secretos nunca salen al
  servidor (no hay JS de cliente que toque Salesforce/Graph).
- **HTMX**: submit del form vía `hx-post` con `hx-target` en un div de resultado; el
  servidor responde con partials Jinja2 (`_success.html` / `_error.html`) que se intercambian.
- **Identidad visual**: Tailwind con tokens `brand` (`#16337D`), `teal` (`#0D9488`),
  `teal-light` (`#F0FAF9`), `smoke` (`#F5F5F5`), `ink`, `muted`, `line` — ver `PALETTE_PREVIEW.html`.

---

## 3. Esquemas de datos — ICT

### 3.1 Constantes (`utils/constants.py` — reutilizado de `pages/utils/constants.py`)
Sin cambios respecto al código actual. Solo se mueve de `pages/utils/` a `utils/`:

```python
COUNTRIES_DICT = {"Mexico": "MX", "USA": "USA", "Canada": "CAD",
                  "Europe": "EUR", "Asia": "ASIA", "Other": "OTHER"}
YES_NO = ["Yes", "No"]
REQ_OPTIONS = ["NA", "Required", "Optional"]
ACTIVATION_TYPES = {"Vacuum box": "OffLine", "Hold down gates": "OffLine",
                    "Pneumatic": "OffLine", "InLine Test Fixture": "InLine"}
WELL_TYPES = ["Single well", "Dual well", "Dual stage"]
SIZE_TYPES = ["Small Kit", "Large Kit", "Small Extended", "Large Extended"]
ICT_FILE_TYPES = [
    "*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)",
    "*BOM",
    "Gerber files",
    "Schematics (pdf)",
    "Test Spec (pdf, doc)",
    "Fixture SOW",
    "Board directory (.tar.gz, .tar)",
]
INVALID_EMAIL_DOMAINS = ["@gmail.com", "@hotmail.com", "@live.com.mx",
                         "@yahoo.com", "@yahoo.com.mx"]
```

### 3.2 WTForms (`app/assessments/forms.py`)
Formulario ICT con Flask-WTF. Una clase por sección + form principal que las compone
(mantén el patrón del `_render_*_section` de Streamlit):

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, \
    TextAreaField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Optional as OptionalV, NumberRange
from utils.constants import (COUNTRIES_DICT, YES_NO, REQ_OPTIONS, ACTIVATION_TYPES,
                             WELL_TYPES, SIZE_TYPES, ICT_FILE_TYPES)
from utils.validators import is_corporate_email

class CorporateEmail(StringField):
    """StringField con validador de email corporativo (no dominios personales)."""
    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data and not is_corporate_email(self.data):
            raise ValueError("Only corporate emails accepted")

class CustomerInfoForm(FlaskForm):
    project_name = StringField("*Name or Project Reference", validators=[DataRequired()])
    contact_name  = StringField("*Contact Name", validators=[DataRequired()])
    customer_name = SelectField("*Company name", choices=[], validate_choice=False)  # se llena desde SF
    customer_name2 = StringField("Company not listed? Write it here.")
    country       = SelectField("*Country", choices=list(COUNTRIES_DICT.keys()))
    quotation_required_date = StringField("When do you need the quote?")  # default JS/Python = hoy+5h
    contact_email = CorporateEmail("*Email", validators=[DataRequired()])
    contact_phone = StringField("Phone Number")
    is_duplicated = RadioField("*Duplicated Project?", choices=YES_NO, default="No")

class FileUploadForm(FlaskForm):
    files = MultipleFileField("Files")
    # checkboxes por tipo: se generan dinámicamente en el template con ICT_FILE_TYPES
    # Se reciben como BooleanField con name="file_type_<slug>"

class IctTechnicalForm(FlaskForm):
    # Feature Fixture
    inline_bottom_side = StringField("For InLine systems, which is the bottom side?")
    activation_type = RadioField("*Activation Type", choices=list(ACTIVATION_TYPES.keys()))
    well_type       = RadioField("*Well Type", choices=WELL_TYPES)
    size_type       = RadioField("*Size Type", choices=SIZE_TYPES)
    fixture_vendor  = StringField("Specify the preferred Fixture Vendor")
    versions        = IntegerField("How many versions?", validators=[NumberRange(min=1)])
    # Flash Programming
    flash_programming = RadioField("Flash Programming?", choices=REQ_OPTIONS)
    programmer_brand  = StringField("What Programmer (Brand) do you want us to use?")
    program_devices   = StringField("Part Numbers of devices to program.")  # split por coma
    logistic_data     = RadioField("(*) Will logistic data be flashed?", choices=YES_NO, default="No")
    items_for_logistic_data = StringField("What kind of info will be stored?")
    # Test Specifications
    test_spec    = RadioField("(*) Do you have Test Spec?", choices=YES_NO, default="No")
    fixture_sow  = RadioField("(*) Do you have Fixture SOW?", choices=YES_NO, default="No")
    config_file  = RadioField("(*) Do you have the config file and codeword data of the 3070?", choices=YES_NO, default="No")
    # Panel
    panel_test      = RadioField("(*) Panel Test?", choices=YES_NO, default="No")
    individual_test = RadioField("(*) Individual Test?", choices=YES_NO, default="No")
    quantity_panel  = IntegerField("Quantity Boards on Panel?", validators=[NumberRange(min=1)])
    quantity_nest   = IntegerField("Specify Nest Qty?", validators=[NumberRange(min=1)])
    # Additional Requirements
    automatic_scanner = RadioField("Automatic Scanner", choices=REQ_OPTIONS)
    scanner_brand     = StringField("Preferred Scanner Brand")
    board_presence    = RadioField("*Board Presence", choices=REQ_OPTIONS)
    window_and_holder = RadioField("Window and Holder for Scanner?", choices=YES_NO, default="No")
    switch_probe_on_connector = RadioField("*Switch probe on connector required?", choices=YES_NO, default="No")
    custom_tests      = RadioField("* Apply Some custom tests?", choices=YES_NO, default="No")
    custom_tests_info = StringField("Specify Custom Test")
    color_test        = RadioField("Color/intensity LED test required?", choices=YES_NO, default="No")
    color_test_info   = StringField("Specify Sensor")
    clock_module      = RadioField("*Clock Mode for Frequency measurement", choices=REQ_OPTIONS)
    testjet           = RadioField("Testjet/VTEP/NanoVTEP", choices=REQ_OPTIONS)
    ics_with_testjet  = StringField("Which ICs are considered to have Testjet/VTEP/NanoVTEP?")
    boundary_scan     = RadioField("*Boundary Scan Test?", choices=REQ_OPTIONS)
    silicon_nails     = RadioField("*Silicon nails and CET?", choices=REQ_OPTIONS)
    required_ics      = StringField("Which ICs are considered in the chain?")

class AdditionalInfoForm(FlaskForm):
    travel = StringField("*Where do you want us to deliver?", validators=[DataRequired()])
    entity_po = StringField("*The entity that the PO will come from.", validators=[DataRequired()])
    additional_comments = TextAreaField("Additional Comments")

class IctForm(CustomerInfoForm, FileUploadForm, IctTechnicalForm, AdditionalInfoForm):
    """Form ICT completo. Hereda todos los campos."""
    pass
```

> `date` (hoy) y `quotation_required_date` (default = hoy + 5 días hábiles) se inyectan
> en el template desde la vista; `date` es hidden, `quotation_required_date` es input date
> con valor por defecto calculado con `utils.dates_info.add_working_days`.

### 3.3 Validaciones extra (server-side, en el orquestador)
- `customer_name == "Other"` → requerir `customer_name2`.
- `program_devices` → split por coma → `program_devices_list`, `quantity_devices = len`.
- `fixure_type = ACTIVATION_TYPES[activation_type]` (derivado, no input).
- Emails personales → rechazo (ya en `CorporateEmail` + `is_corporate_email`).

---

## 4. Contratos de rutas Flask

### `GET /assessments/ict`
- **Auth**: `@login_required`.
- **Render**: `assessments/ict/form.html` con `IctForm()` + `accounts` (de `/api/accounts`
  o directamente del servicio cacheado) + `today` + `quotation_default_date`.
- **Response**: HTML 200.

### `POST /assessments/ict/submit`
- **Auth**: `@login_required`.
- **Content-Type**: `multipart/form-data` (form + archivos).
- **HTMX**: el form envía con `hx-post="/assessments/ict/submit"` y
  `hx-target="#result"`, `hx-swap="innerHTML"`. El servidor responde con un partial.
- **Respuestas** (todas devuelven un partial HTML para HTMX, **no** redirects):
  - **200** → `_success.html`: toast verde con `opportunity_id` + link a SharePoint.
  - **422** → `_error.html`: toast rojo con `error_code=VALIDATION` + lista de errores de
    WTForms (campos resaltados via `hx-post` re-render del form con errores).
  - **409** → `_error.html`: `error_code=DUPLICATE`.
  - **502/503** → `_error.html`: `error_code=SALESFORCE` / `STORAGE`.
- **Side effects** (orquestador §6.4): carpeta+plantilla, archivos, HTML, Opportunity, audit.

### `GET /api/accounts`
- **Auth**: `@login_required`.
- **Query**: `?format=partial` (default, HTMX options) o `?format=json`.
- **Response partial**: `<option>` tags para inyectar en el `<select>` (HTMX `hx-get` al
  foco del select). Cacheado 10 min server-side.
- **Response JSON**: `[{id, name}, ...]` ordenado A-Z + `Other` al final.
- **503**: si Salesforce no responde tras reintentos → `[{id: "other", name: "Other"}]`
  (mismo fallback que `get_unique_account_dict()` actual).

---

## 5. Modelo de datos — `SubmissionsAudit` (SQLAlchemy)

Tabla nueva (Fase 0 creó `db` y migraciones base; aquí se añade):

```python
# app/models/submission.py
from datetime import datetime
from app.models import db

class SubmissionsAudit(db.Model):
    __tablename__ = "submissions_audit"
    id            = db.Column(db.String(36), primary_key=True)  # UUID
    assessment_type = db.Column(db.String(8), nullable=False)   # "ICT"|"FCT"|"IAT"
    status        = db.Column(db.String(16), nullable=False)    # success|failed|in_progress
    payload       = db.Column(db.JSON, nullable=False)          # form data completo
    error_code    = db.Column(db.String(16))                     # VALIDATION|STORAGE|SALESFORCE|DUPLICATE|UNKNOWN
    error_message = db.Column(db.Text)
    salesforce_opportunity_id = db.Column(db.String(32))
    sharepoint_url = db.Column(db.String(512))
    project_path  = db.Column(db.String(512))
    file_count    = db.Column(db.Integer, default=0)
    user_id       = db.Column(db.String(36))                     # cuenta local (nullable para SSO)
    user_email    = db.Column(db.String(255), nullable=False)
    auth_method   = db.Column(db.String(16), nullable=False)     # azure_ad|credentials
    duration_ms   = db.Column(db.Integer)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index("ix_audit_bu_status_date", "assessment_type", "status", "created_at"),
        db.Index("ix_audit_email_date", "user_email", "created_at"),
    )
```

**Política de escritura** (`app/services/audit.py`):
- `start_audit(assessment_type, payload, user, file_count)` → inserta `in_progress`, retorna `id`.
- `finish_audit(id, status, **fields)` → actualiza con resultado / error / parcial.
- Se escribe en **todos** los caminos de error (incluido 422 de validación).

---

## 6. Servicios (reutilizados + nuevos)

### 6.1 `services/salesforce_service.py` (★ reutilizado)
Cambios mínimos:
- Quitar `@st.cache_resource` / `@st.cache_data` (reemplazar con `cachetools.func.ttl_cache`
  o un `lru_cache` con TTL casero; mantener TTL de 10 min para `get_accounts`).
- Quitar `import streamlit as st`.
- Mantener `retry_on_timeout` (backoff exponencial 2→30s, máx 3) **sin cambios**.
- Mantener `create_opportunity()` con campos `BU__c`, `Path__c`, `Assessment_Date__c`.

### 6.2 `services/storage_service.py` + `storage/*` (★ reutilizados)
- Quitar `@st.cache_resource` de `get_storage_service()`.
- `StorageProvider` (base), `LocalStorageProvider`, `SharePointStorageProvider` **sin cambios**.
- `copy_template()` de SharePoint se mantiene (archivo por archivo); upload resumible es Fase 3.

### 6.3 `app/services/audit.py` (nuevo)
Capa fina sobre `SubmissionsAudit` (ver §5). Sin lógica de negocio.

### 6.4 `app/assessments/orchestrator.py` (nuevo — derivado de `BaseAssessment`)
Equivalente a `BaseAssessment.process_form_submission` pero sin `st.*` y con auditoría:

```python
from datetime import datetime
from pathlib import Path
from services.salesforce_service import get_salesforce_service, get_unique_account_dict
from services.storage_service import get_storage_service
from utils.constants import COUNTRIES_DICT, ACTIVATION_TYPES
from utils.dates_info import get_last_weekday_of_next_month
from app.assessments.report import render_ict_report
from app.services.audit import start_audit, finish_audit
from core.exceptions import ValidationError, StorageError, SalesforceError
import core.logging_config
from core.logging_config import get_logger

logger = get_logger(__name__)

def process_ict_submission(form: IctForm, files: list, user) -> dict:
    """
    Orquesta el submit ICT. Retorna dict con success/error para la vista.
    Lanza excepciones tipadas que la ruta mapea a HTTP/partial HTMX.
    """
    audit_id = start_audit("ICT", form.data, user, len(files))
    t0 = time.time()
    try:
        # 1. Validar form (WTForms ya validó en ruta; aquí validación extra de negocio)
        if form.customer_name.data in (None, "Other") and not form.customer_name2.data:
            raise ValidationError("Customer name is required", field="customer_name2")

        # 2. Construir info dict (espejo de self.info en BaseAssessment)
        info = build_info_from_form(form)  # incluye derivados: fixure_type, quantity_devices

        # 3. Preparar customer_data
        customer_data = prepare_customer_data(form)

        # 4. Crear carpeta + plantilla + subir archivos
        storage = get_storage_service()
        project_path = storage.create_project_folder(
            assessment_type="ICT",
            projects_folder="1_In_Circuit Test (ICT)",
            customer_name=customer_data["customer_name"],
            project_name=info["project_name"],
            country=customer_data["country"],
        )
        if files:
            storage.upload_assessment_files(project_path, "ICT", files)

        # 5. Generar + guardar HTML
        html = render_ict_report(info)
        storage.save_assessment_html(project_path, "ICT", html)

        # 6. SharePoint URL
        sharepoint_url = build_sharepoint_url(project_path)

        # 7. Opportunity en Salesforce
        sf = get_salesforce_service()
        account_id = customer_data.get("account_id")
        result = sf.create_opportunity(
            name=info["project_name"], stage_name="New Request",
            close_date=get_last_weekday_of_next_month().strftime("%Y-%m-%d"),
            assessment_date=datetime.now().strftime("%Y-%m-%d"),
            path=sharepoint_url, bu="ICT", account_id=account_id,
        )
        if not result.get("success"):
            raise SalesforceError(f"SF rejected: {result.get('errors')}")

        finish_audit(audit_id, "success",
                     salesforce_opportunity_id=result.get("id"),
                     sharepoint_url=sharepoint_url, project_path=project_path,
                     duration_ms=int((time.time()-t0)*1000))
        return {"success": True, "opportunity_id": result["id"], "sharepoint_url": sharepoint_url}

    except (ValidationError, StorageError, SalesforceError) as e:
        finish_audit(audit_id, "failed", error_code=e.__class__.__name__.upper().replace("ERROR",""),
                     error_message=str(e), duration_ms=int((time.time()-t0)*1000))
        raise
    except Exception as e:
        logger.exception("Unexpected error in ICT submission")
        finish_audit(audit_id, "failed", error_code="UNKNOWN", error_message=str(e))
        raise
```

**Helper `build_info_from_form(form) -> dict`**: convierte el form WTForms al dict `info`
que espera `render_ict_report` (espejo de los `self.info[...]` del código actual), aplicando
derivaciones:
- `fixure_type = ACTIVATION_TYPES[activation_type]`
- `program_devices = [p.strip() for p in program_devices_str.split(",") if p.strip()]`
- `quantity_devices = len(program_devices)`
- `file_types = {tipo: bool(form["file_type_<slug>"].data) for tipo in ICT_FILE_TYPES}`

**Helper `build_sharepoint_url(project_path)`**: reemplaza `_get_sharepoint_url` de
`base_assessment_refactored.py:261` (corrigiendo el bug del `Path` no importado — usar
`pathlib.PurePosixPath`).

### 6.5 `app/assessments/report.py` + `templates/reports/ict_report.html` (nuevo)
Reemplaza `pages/utils/ict_create_html.py` (f-strings) por Jinja2:

```python
# app/assessments/report.py
from flask import render_template_string  # o render_template con carpeta dedicada

def render_ict_report(info: dict) -> str:
    """Render del HTML report ICT (mismo contenido que ict_create_html.py)."""
    return render_template_string(ICT_REPORT_TEMPLATE, data=info, now=datetime.now())
```

O mejor, `render_template("reports/ict_report.html", data=info)` con el template en
`app/templates/reports/ict_report.html` — estructura 1:1 con el actual (Header, Contact,
Technical, Programming, Testing, Additional, Miscellaneous, Footer) pero en Jinja2 con la
**misma paleta corporativa** (Tailwind tokens `brand`/`teal`). Mantiene
`<script src="https://cdn.tailwindcss.com">` como hoy para que el archivo sea
self-contained al abrirlo fuera de la app.

---

## 7. UI — Templates con paleta corporativa

> Referencia visual: `PALETTE_PREVIEW.html`. Todos los templates extienden `base.html`
> (de Fase 0) que ya tiene el header DarkBlue + logo + nav + logout.

### 7.1 `assessments/_macros_common.html`
Macros Jinja2 reutilizables por BU (Fase 2 los reusa para FCT/IAT):

```jinja2
{# Sección de customer info (común) #}
{% macro customer_info(form, accounts) %}
<section class="bg-white rounded-card shadow-card p-6">
  <h2 class="text-lg font-semibold text-brand border-b border-line pb-3 mb-4">
    {{ _('assessments.common.customerInfo') }}
  </h2>
  <p class="text-sm text-muted mb-4">(*) {{ _('Mandatory Fields') }}</p>
  <div class="grid grid-cols-2 gap-4">
    {{ field(form.project_name, "text") }}
    {{ field(form.contact_name, "text") }}
    <div>
      {{ form.customer_name.label(class_="block text-sm font-medium text-muted mb-1") }}
      {{ form.customer_name(class_="w-full rounded-field border border-line bg-smoke px-3 py-2 text-sm focus:bg-white") }}
    </div>
    {# ... resto de campos ... #}
  </div>
</section>
{% endmacro %}

{# Uploader + checkboxes de tipos (común) #}
{% macro file_upload(form, file_types) %}
<section class="bg-white rounded-card shadow-card p-6">
  <h2 class="text-lg font-semibold text-brand border-b border-line pb-3 mb-4">
    {{ _('assessments.files.title') }}
  </h2>
  <input type="file" name="files" multiple
    class="block w-full text-sm text-muted file:mr-3 file:py-2 file:px-4 file:rounded-field file:border-0 file:bg-teal file:text-white">
  <div class="mt-3 space-y-1.5">
    {% for ft in file_types %}
      {% set slug = ft | slugify %}
      <label class="flex items-center gap-2 text-sm">
        <input type="checkbox" name="file_type_{{ slug }}" value="1"
          {% if ft.startswith("*") %}checked{% endif %} class="accent-teal">
        <span>{{ ft }}</span>
      </label>
    {% endfor %}
  </div>
</section>
{% endmacro %}
```

### 7.2 `assessments/ict/_sections.html`
Las 5 secciones técnicas ICT (espejo de `_render_*_section`):

| Macro / bloque | Origen Streamlit |
|----------------|------------------|
| `feature_fixture_section(form)` | `_render_feature_fixture_section` |
| `flash_programming_section(form)` | `_render_flash_programming_section` (collapsible `<details>`) |
| `test_specifications_section(form)` | `_render_test_specifications_section` |
| `panel_section(form)` | `_render_panel_section` |
| `additional_requirements_section(form)` | `_render_additional_requirements_section` (incluye `<details>` Boundary Scan) |

Radios horizontales: WTForms `RadioField(render_kw={"class": "accent-teal inline-flex"})`
con CSS `flex gap-4`. Selects con `placeholder` via primer `<option value="" disabled selected>`.

### 7.3 `assessments/ict/form.html`
```jinja2
{% extends "base.html" %}
{% block title %}{{ _('assessments.ict.title') }}{% endblock %}

{% block content %}
<h1 class="text-2xl font-bold text-brand mb-6">{{ _('assessments.ict.title') }}</h1>

<form method="POST" action="{{ url_for('assessments.submit_ict') }}"
      enctype="multipart/form-data"
      hx-post="{{ url_for('assessments.submit_ict') }}"
      hx-target="#result" hx-swap="innerHTML"
      hx-encoding="multipart/form-data">
  {{ form.hidden_tag() }}
  {{ macros.customer_info(form, accounts) }}
  {{ macros.file_upload(form, ICT_FILE_TYPES) }}
  {% include "assessments/ict/_sections.html" %}
  {{ macros.additional_info(form) }}

  <div class="flex gap-3 mt-6">
    <button type="submit" class="px-5 py-2 rounded-field bg-brand text-white font-semibold
             hover:bg-brand-hover transition">{{ _('assessments.submit') }}</button>
    <a href="{{ url_for('auth.logout') }}"
       class="px-5 py-2 rounded-field border border-teal text-teal font-semibold
       hover:bg-teal-tint transition">{{ _('assessments.logout') }}</a>
  </div>
</form>

<div id="result" class="mt-4"></div>  {# aquí HTMX inyecta _success/_error #}
{% endblock %}
```

### 7.4 `assessments/ict/_success.html` (partial HTMX)
```jinja2
<div class="rounded-field border border-green-200 bg-green-50 text-green-800 px-4 py-3 text-sm flex items-center gap-2">
  <span>✅</span>
  <span>{{ _('assessments.result.success') }}</span>
  <span class="font-mono text-xs ml-2">{{ opportunity_id }}</span>
  <a href="{{ sharepoint_url }}" target="_blank"
     class="ml-auto text-teal underline">Open in SharePoint →</a>
</div>
```

### 7.5 `assessments/_error.html` (partial HTMX)
```jinja2
<div class="rounded-field border px-4 py-3 text-sm flex items-center gap-2
            {% if error_code == 'VALIDATION' %}border-amber-200 bg-amber-50 text-amber-800
            {% else %}border-red-200 bg-red-50 text-danger{% endif %}">
  <span>{% if error_code == 'VALIDATION' %}⚠️{% else %}❌{% endif %}</span>
  <div>
    <div>{{ _(('assessments.result.error.%s' % error_code|lower), message=message) }}</div>
    {% if details %}<ul class="list-disc ml-5 mt-1 text-xs">{% for d in details %}<li>{{ d }}</li>{% endfor %}</ul>{% endif %}
  </div>
</div>
```

### 7.6 Reporte HTML `reports/ict_report.html`
Estructura 1:1 con `ict_create_html.py` (7 secciones + footer), con Tailwind + tokens
`brand`/`teal`, fuente Inter, mismo `<script src="https://cdn.tailwindcss.com">` para
ser self-contained al abrirlo en SharePoint. El `render_ict_report(info)` lo renderiza a
string y se guarda como `ICT_Assessment.html` en la carpeta del proyecto.

---

## 8. i18n — Flask-Babel (ES/EN)

Fase 0 instaló Flask-Babel. Fase 1 añade las claves ICT en `translations/es/LC_MESSAGES/messages.po`
y `translations/en/LC_MESSAGES/messages.po` (o `.json` según config de Fase 0):

```po
msgid "assessments.ict.title"
msgstr "In Circuit Test Assessment"   # EN
msgstr "Evaluación In Circuit Test"   # ES

msgid "assessments.ict.featureFixture.title"
msgstr "Feature Fixture"

msgid "assessments.common.projectName"
msgstr "*Name or Project Reference"
msgstr "*Nombre o Referencia del Proyecto"

msgid "assessments.result.success"
msgstr "Opportunity created successfully!"
msgstr "¡Oportunidad creada exitosamente!"

msgid "assessments.result.error.duplicate"
msgstr "Project already exists. Contact Sales Manager."
msgstr "El proyecto ya existe. Contacta al Sales Manager."
# ... etc (ver §8 del plan Next.js, mismas claves adaptadas)
```

**Regla**: **labels de UI traducidos**; **valores técnicos** (guardados en reporte HTML y
Salesforce) permanecen en **EN** (ej. `Yes`/`No`, `Single well`, `OffLine`). Esto evita
romper el reporte que ve el cliente ni los campos `BU__c`/`StageName` de SF.

---

## 9. Tareas en waves (con dependencias)

### Wave A — Fundamentos ICT (sin dependencias entre sí)

**A1. Mover utils + limpiar st.* de servicios**
- Dep: —
- Archivos: mover `pages/utils/{constants,dates_info,validations}.py` → `utils/`;
  editar `services/salesforce_service.py` y `services/storage_service.py` (quitar
  `@st.cache_*` e `import streamlit`; reemplazar caché por `cachetools.func.ttl_cache`);
  editar `config/settings.py` (quitar refs a `st.secrets`, solo dotenv).
- CA: `python -c "from services.salesforce_service import get_unique_account_dict; print(len(get_unique_account_dict()))"`
  funciona sin Streamlit instalado; `from utils.validators import is_corporateEmail` OK.

**A2. Modelo `SubmissionsAudit` + Alembic**
- Dep: — (usa `db` de Fase 0).
- Archivos: `app/models/submission.py`, migración Alembic, `app/services/audit.py`.
- CA: `flask db upgrade` aplica la tabla; `audit.start_audit(...)` inserta
  `in_progress`; `audit.finish_audit(id, status="success", ...)` actualiza; query retorna
  el registro.

**A3. WTForms ICT**
- Dep: A1 (utils/constants).
- Archivos: `app/assessments/forms.py` (IctForm + secciones + CorporateEmail).
- CA: `IctForm()` con datos válidos `validate_on_submit()` → True; email `@gmail.com`
  → False con error "Only corporate emails accepted"; campos `*` vacíos → False.

### Wave B — Backend de datos y reporte (dep. A1)

**B1. Reporte HTML ICT (Jinja2)**
- Dep: A1.
- Archivos: `app/assessments/report.py`, `app/templates/reports/ict_report.html`.
- CA: `render_ict_report(info_fixture)` produce HTML con 7 secciones; al guardarlo y
  abrir en navegador muestra estilos Tailwind con paleta iBtest; un snapshot test cubre
  estructura y tokens de color.

### Wave C — Orquestador y rutas (dep. A1, A2, A3, B1)

**C1. Orquestador `orchestrator.py`**
- Dep: A1, A2, A3, B1 (usa servicios reutilizados + report + audit).
- Archivos: `app/assessments/orchestrator.py` (+ helpers `build_info_from_form`,
  `prepare_customer_data`, `build_sharepoint_url`).
- CA: contra SF sandbox + SharePoint test, un payload+archivos de fixture produce: carpeta
  con `TEMPLATE_ICT`, archivo en `7_ALL_Info_Shared`, `ICT_Assessment.html`, Opportunity
  en SF, audit `success`. Casos: duplicado (StorageError → 409), SF caído (mock → audit
  `failed` con `project_path` lleno). Derivaciones (`fixure_type`, `quantity_devices`)
  correctas en el HTML. **Bug de `Path` no importado corregido**.

**C2. `GET /api/accounts`**
- Dep: A1.
- Archivos: `app/api/accounts.py`, blueprint `api_bp`.
- CA: autenticado → 200 + lista cacheada (segunda llamada < primera); no auth → 401;
  SF caído → 200 con solo `[{id:"other", name:"Other"}]` (fallback). `?format=partial`
  devuelve `<option>` tags; `?format=json` devuelve JSON.

**C3. `POST /assessments/ict/submit` + `GET /assessments/ict`**
- Dep: C1, C2, A2, A3.
- Archivos: `app/assessments/routes.py`, blueprint `assessments_bp`.
- CA: `GET` renderiza el form con accounts cargadas; `POST` multipart válido → 200 +
  partial `_success` con `opportunity_id`; form inválido → 422 + `_error` con `details`;
  carpeta existente → 409 + `_error` DUPLICATE; SF caído → 503 + `_error` SALESFORCE.
  Audit se escribe en **todos** los casos (incluso 422).

### Wave D — UI + HTMX (dep. C3)

**D1. Macros comunes + secciones ICT**
- Dep: A3.
- Archivos: `app/templates/assessments/_macros_common.html`,
  `app/templates/assessments/ict/_sections.html`.
- CA: render con `IctForm` fixture muestra todas las secciones; radios horizontales,
  collapsibles (`<details>`), selects con placeholder; clases Tailwind con tokens
  `brand`/`teal`/`smoke` (visual = `PALETTE_PREVIEW.html`).

**D2. Página ICT + submit HTMX + partials**
- Dep: D1, C3.
- Archivos: `app/templates/assessments/ict/form.html`,
  `app/templates/assessments/ict/_success.html`, `app/templates/assessments/_error.html`,
  `app/static/js/assessments.js` (split por coma de program_devices, etc.).
- CA: flujo manual completo contra entorno de prueba: login → llenar ICT → subir archivo
  → submit → toast verde con `opportunity_id` + link. Logout funciona. Errores muestran
  toasts i18n correctos.

**D3. i18n ICT**
- Dep: D1.
- Archivos: `translations/{en,es}/LC_MESSAGES/messages.po` (claves ICT).
- CA: cambiar locale ES↔EN traduce labels; valores técnicos (Yes/No, Single well)
  permanecen EN. Sin claves sin traducir (ejecutar `pybabel extract + update + compile`).

### Wave E — Verificación E2E (dep. C3, D2, D3)

**E1. Pruebas E2E contra entorno de pruebas**
- Dep: D2, D3, C3.
- Archivos: `tests/` (pytest + maybe Flask test client + mocks SF/SP).
- CA: checklist de aceptación (§10) completo pasado contra SF sandbox + SharePoint test.
  Cobertura: flujo éxito, duplicado, validación, SF caído (mock), ES/EN.

**E2. Runbook de la Fase 1**
- Dep: E1.
- Archivos: `docs/phase-1-runbook.md` (env vars, deploy Easypanel, verificación).
- CA: otro miembro del equipo despliega y verifica la Fase 1 sin ayuda.

---

## 10. Criterios de aceptación de la Fase 1 (UAT)

Verificación end-to-end contra **Salesforce sandbox** + **SharePoint de prueba**:

1. **Login**: usuario interno (Azure AD) y externo (cuenta local) acceden a
   `/assessments/ict`.
2. **Accounts**: el `<select>` de cliente carga desde `/api/accounts`, ordenado A-Z, con
   "Other" al final; segunda carga usa caché.
3. **Form ICT**: todas las secciones renderizan con labels ES y EN; campos `*` marcan
   error al submitir vacíos; email `@gmail.com` se rechaza con mensaje i18n.
4. **Submit exitoso** (vía HTMX):
   - Se crea `{basePath}/1_In_Circuit Test (ICT)/{country}/{customer}/{project}/` con la
     plantilla `TEMPLATE_ICT` copiada.
   - Los archivos del cliente quedan en `.../1_Customer_Info/7_ALL_Info_Shared/`.
   - Existe `ICT_Assessment.html` en la raíz del proyecto, abre en navegador y muestra las
     7 secciones con los datos enviados, con paleta iBtest (DarkBlue headers, teal acentos).
   - Se crea `Opportunity` con `StageName="New Request"`, `BU__c="ICT"`,
     `Path__c` = URL de SharePoint del proyecto, `CloseDate` = último día hábil del mes
     siguiente, `AccountId` si el cliente estaba en la lista.
   - `submissions_audit` tiene un registro `success` con `opportunity_id`,
     `sharepoint_url`, `project_path`, `duration_ms`, `user_email`, `auth_method`.
   - Toast verde (`_success.html`) muestra `opportunity_id` + link a SharePoint.
5. **Cliente no listado**: Opportunity se crea **sin** `AccountId`; `customer_name2` se
   usa como nombre.
6. **Proyecto duplicado**: submit con `project_name` ya existente → 409 + toast i18n;
   audit `failed` con `error_code=DUPLICATE`; no se crea nada en SF.
7. **Salesforce caído** (mock): carpeta+archivos+HTML creados, Opportunity falla → audit
   `failed` con `error_code=SALESFORCE` y `project_path` lleno; toast i18n.
8. **Validación**: email personal o campos requeridos vacíos → 422 + `_error` con
   `details[]`; audit `failed` con `error_code=VALIDATION`; nada se crea en storage/SF.
9. **i18n**: todo el flujo en ES y EN sin claves sin traducir; valores técnicos en EN.
10. **Logout**: cierra sesión y redirige a login.
11. **Identidad visual**: la UI y el `ICT_Assessment.html` coinciden con la paleta de
    `PALETTE_PREVIEW.html` (DarkBlue primario, teal acento, fondo teal-light, tarjetas
    blancas con sombra).

---

## 11. Stack y dependencias (requirements.txt — adiciones a Fase 0)

```text
# Flask core (de Fase 0)
Flask>=3.0
Flask-Login>=0.6
Flask-WTF>=1.2
Flask-Babel>=4.0
flask-SQLAlchemy>=3.1
authlib>=1.3
bcrypt>=4.1

# Reutilizados del proyecto actual (sin Streamlit)
simple-salesforce>=1.12
msal>=1.34
requests>=2.32
python-dotenv>=1.1
cachetools>=5.3        # reemplaza st.cache_* con TTL
tenacity>=8.2          # opcional, si se migra retry a tenacity (mantiene retry_on_timeout actual)

# DB / migraciones
SQLAlchemy>=2.0
alembic>=1.13
psycopg2-binary>=2.9   # PostgreSQL

# Testing (no prod)
pytest>=8.0
pytest-flask>=1.3
responses>=0.25        # mocks HTTP para SF/Graph
```

> `streamlit`, `altair`, `pandas`, `pyarrow`, `pillow` (Streamlit deps) **ya no se requieren**.

---

## 12. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| `simple-salesforce` funciona distinto fuera de Streamlit (sin `@st.cache`) | Probar `get_accounts`/`create_opportunity` al principio (Wave A1) con caché `cachetools`. Bajo riesgo: el cliente es el mismo. |
| `copyTemplate` SharePoint lento/falla a mitad (igual que hoy) | Mantener comportamiento en Fase 1; registrar progreso en audit; transaccionalidad completa es Fase 3. |
| Upload >4MB sin sesión resumible | Documentar límite efectivo (4MB por archivo simple); upload resumible es Fase 3. UI puede advertir si supera 4MB. |
| Caché de Accounts entre workers gunicorn | TTL en memoria por worker (aceptable para ~50 cuentas); Redis queda para Fase 3 si se necesita coherencia. |
| Auth híbrida: cuentas locales sin flujo de invitación | Fase 0 debe entregar alta de cuentas locales; si no, usar solo Azure AD para E2E de Fase 1 y diferir externos. |
| Reporte HTML con Tailwind CDN depende de internet al abrir | Decisión menor: inline de Tailwind compilado en el render (sin CDN) para offline. Mismo enfoque ya usado hoy. |
| CSRF + multipart con HTMX | Flask-WTF maneja CSRF; verificar token en POST HTMX. Si HTMX no envía el token por defecto, incluir `X-CSRFToken` header via `htmx:configRequest`. |

> Comparado con el plan Next.js anterior: **3 riesgos críticos desaparecen** (jsforce
> incompatibilidad, `react-dom/server` cold start, secretos server/client). Los
> restantes son del dominio del problema (SharePoint, auth), no del stack.

---

## 13. Notas de implementación

- **Reutilización real**: ~70% del backend (services, storage, core, config, utils) se
  mueve sin tocar la lógica, solo limpiando `st.*`. Verificar con imports al final de A1.
- **`build_sharepoint_url`**: usar `pathlib.PurePosixPath` (no `Path` que rompe en Windows
  para URLs). Corrige el bug `base_assessment_refactored.py:279` (`Path` no importado).
- **Derivaciones antes del HTML**: `fixure_type`, `quantity_devices`, `file_types` dict
  se calculan en `build_info_from_form` y se añaden al `info` antes de renderizar.
- **HTMX + CSRF**: configurar `htmx.config` global o por-request para inyectar el header
  `X-CSRFToken` (Flask-WTF expone el token en el template). Alternativa: desactivar CSRF
  solo para la ruta `/submit` y validar origin — **no recomendado**.
- **Tests**: priorizar `test_orchestrator_ict.py` (C1) y `test_api_submit_ict.py` (C3)
  con `responses` para mockear SF/Graph. UI con test de render del form (D1).
- **Idempotencia**: no hay en Fase 1 (igual que hoy). Un re-submit del mismo
  `project_name` tras fallo parcial → 409. Documentarlo en el runbook.
- **Quotation date**: el default se calcula server-side con `add_working_days(today, 5)`
  y se pasa al template; el input `<input type="date" value="{{ quotation_default_date }}">`
  permite override del usuario.

---

*Plan ejecutable de la Fase 1 (Flask + Jinja2 + HTMX). Siguiente paso: confirmar Fase 0
iniciada/completada y arrancar el Wave A.*
