# ⚡ Guía Rápida de Despliegue en Streamlit Cloud

## 🚀 Pasos Rápidos

### **1. Generar secrets.toml automáticamente**

```bash
python scripts/convert_env_to_secrets.py
```

Esto crea `.streamlit/secrets.toml` desde tu `.env` actual.

---

### **2. Revisar el archivo generado**

```bash
nano .streamlit/secrets.toml
```

**⚠️ IMPORTANTE:** Verifica que el `client_secret` sea el NUEVO (rotado), no el expuesto en Git.

---

### **3. Subir código a GitHub (si no lo has hecho)**

```bash
git add .
git commit -m "Add Streamlit Cloud support"
git push origin main
```

---

### **4. Desplegar en Streamlit Cloud**

1. **Ve a:** https://share.streamlit.io/
2. **Click:** "New app"
3. **Selecciona:**
   - Repository: `angel88c/sf-assesments`
   - Branch: `main`
   - Main file: `main.py`
4. **Click:** "Advanced settings"
5. **Pega** todo el contenido de `.streamlit/secrets.toml` en la sección "Secrets"
6. **Click:** "Deploy!"

---

### **5. Verificar**

Espera a que la app se despliegue y prueba:
- ✅ Login funciona
- ✅ Crear assessment
- ✅ Conexión a Salesforce
- ✅ Subida a SharePoint

---

## 🔧 Comando Útiles

### **Convertir .env a secrets.toml:**
```bash
python scripts/convert_env_to_secrets.py
```

### **Ver contenido de secrets.toml:**
```bash
cat .streamlit/secrets.toml
```

### **Verificar que secrets.toml NO está en Git:**
```bash
git ls-files | grep secrets.toml
# Solo debería mostrar: secrets.toml.example
```

---

## 📋 Checklist Rápido

- [ ] Ejecutar `convert_env_to_secrets.py`
- [ ] Revisar `.streamlit/secrets.toml`
- [ ] Verificar que usa client_secret NUEVO (rotado)
- [ ] Push a GitHub
- [ ] Crear app en Streamlit Cloud
- [ ] Copiar secrets al dashboard
- [ ] Deploy
- [ ] Probar la aplicación

---

## ⚠️ Recordatorios

1. **NUNCA** commites `.streamlit/secrets.toml` a Git
2. **USA** el client_secret NUEVO (el anterior fue expuesto)
3. **VERIFICA** que la app funciona localmente antes de desplegar
4. **MANTÉN** tu `.env` local para desarrollo

---

## 🐛 Problemas Comunes

**App no carga:**
- Verifica que pusheaste el código
- Revisa logs en Streamlit Cloud dashboard

**Error de autenticación:**
- Verifica secrets en Streamlit Cloud
- Asegúrate de copiar TODO el contenido de secrets.toml

**Falta alguna variable:**
- Agrega la variable en Streamlit Cloud → Settings → Secrets
- Usa el formato TOML: `[section] key = "value"`

---

## 📚 Documentación Completa

Ver `STREAMLIT_DEPLOYMENT.md` para detalles completos.

---

## ✅ ¡Listo!

Tu aplicación ahora funciona en:
- **Local:** `.env` (desarrollo)
- **Cloud:** `secrets.toml` (producción)

El código detecta automáticamente el entorno. 🎉
