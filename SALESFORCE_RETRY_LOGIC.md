# 🔄 Salesforce Retry Logic - Manejo de Timeouts

## 🎯 Problema

Error común al crear oportunidades en Salesforce:
```
Failed to create opportunity: HTTPSConnectionPool(host='login.salesforce.com', port=443): 
Read timed out. (read timeout=40)
```

## ✅ Solución Implementada

### **1. Retry con Exponential Backoff**

Se implementó un decorador `@retry_on_timeout` que automáticamente reintenta las operaciones cuando hay timeouts o errores de conexión.

#### **Características:**
- ✅ **Reintentos automáticos** cuando hay timeout/conexión
- ✅ **Exponential backoff** - Cada reintento espera más tiempo
- ✅ **Máximo de reintentos configurable** (default: 3)
- ✅ **Logs detallados** de cada reintento
- ✅ **Solo para errores recuperables** (timeout, conexión)

### **2. Métodos con Retry Logic**

Los siguientes métodos tienen retry automático:

| Método | Descripción | Reintentos |
|--------|-------------|------------|
| `create_opportunity()` | Crea oportunidad en Salesforce | 3 intentos |
| `get_accounts()` | Obtiene lista de cuentas | 3 intentos |

## 🔧 Cómo Funciona

### **Ejemplo de Flujo con Timeout:**

```
1️⃣ Intento 1: create_opportunity()
   ❌ Timeout después de 40 segundos
   ⏳ Esperando 2 segundos...

2️⃣ Intento 2: create_opportunity()
   ❌ Timeout después de 40 segundos
   ⏳ Esperando 4 segundos...

3️⃣ Intento 3: create_opportunity()
   ❌ Timeout después de 40 segundos
   ⏳ Esperando 8 segundos...

4️⃣ Intento 4: create_opportunity()
   ✅ Éxito! Oportunidad creada
```

### **Exponential Backoff:**

```python
Intento 1 → Falla → Espera 2 segundos
Intento 2 → Falla → Espera 4 segundos (2 * 2^1)
Intento 3 → Falla → Espera 8 segundos (2 * 2^2)
Intento 4 → Falla → Espera 16 segundos (2 * 2^3)
...
Máximo: 30 segundos de espera
```

## 📊 Configuración

### **Variables del Decorador:**

```python
@retry_on_timeout(
    max_retries=3,      # Número máximo de reintentos (default: 3)
    base_delay=2.0,     # Delay inicial en segundos (default: 2.0)
    max_delay=30.0      # Delay máximo en segundos (default: 30.0)
)
```

### **Timeout de Salesforce (.env):**

```bash
# Timeout para operaciones de Salesforce (segundos)
SALESFORCE_TIMEOUT=40  # Default: 40 segundos
```

## 📋 Recomendaciones

### **1. Si los Timeouts son Frecuentes:**

#### **Opción A: Aumentar Timeout**
```bash
# En .env
SALESFORCE_TIMEOUT=60  # Aumentar a 60 segundos
```

**Pros:**
- Menos timeouts
- Más tiempo para completar operación

**Contras:**
- Usuario espera más tiempo

#### **Opción B: Aumentar Reintentos**
```python
# En services/salesforce_service.py
@retry_on_timeout(max_retries=5, base_delay=2.0, max_delay=30.0)
def create_opportunity(...):
```

**Pros:**
- Más oportunidades de éxito
- Maneja mejor problemas transitorios

**Contras:**
- Puede tardar mucho tiempo total

#### **Opción C: Reducir Base Delay**
```python
@retry_on_timeout(max_retries=3, base_delay=1.0, max_delay=15.0)
```

**Pros:**
- Reintentos más rápidos
- Menor tiempo total de espera

**Contras:**
- Puede no dar suficiente tiempo para recuperarse

### **2. Configuración Recomendada por Escenario**

#### **🌐 Conexión Inestable (Frecuentes Timeouts):**
```python
@retry_on_timeout(max_retries=5, base_delay=3.0, max_delay=45.0)
```
```bash
SALESFORCE_TIMEOUT=60
```

#### **🏢 Red Corporativa Estable:**
```python
@retry_on_timeout(max_retries=3, base_delay=2.0, max_delay=30.0)  # Default
```
```bash
SALESFORCE_TIMEOUT=40  # Default
```

#### **🚀 Ambiente de Producción (Alta Disponibilidad):**
```python
@retry_on_timeout(max_retries=4, base_delay=2.0, max_delay=30.0)
```
```bash
SALESFORCE_TIMEOUT=50
```

## 📝 Logs

### **Ejemplo de Logs con Retry:**

```
2025-10-14 11:20:15 - INFO - Creating opportunity: Test Project
2025-10-14 11:20:55 - WARNING - Timeout/Connection error on create_opportunity 
                                 (attempt 1/4). Retrying in 2.0 seconds... 
                                 Error: Read timed out. (read timeout=40)
2025-10-14 11:20:57 - INFO - Creating opportunity: Test Project
2025-10-14 11:21:37 - WARNING - Timeout/Connection error on create_opportunity 
                                 (attempt 2/4). Retrying in 4.0 seconds... 
                                 Error: Read timed out. (read timeout=40)
2025-10-14 11:21:41 - INFO - Creating opportunity: Test Project
2025-10-14 11:21:50 - INFO - Successfully created opportunity: 006Rl000013pGwX
```

## 🔍 Errores que SÍ Reintenta

- ✅ `Timeout` - Timeout de lectura/escritura
- ✅ `ConnectionError` - Error de conexión de red
- ✅ `HTTPSConnectionPool` timeouts

## ❌ Errores que NO Reintenta

- ❌ Errores de validación de Salesforce
- ❌ Errores de autenticación
- ❌ Errores de datos (campos incorrectos)
- ❌ Excepciones generales de Python

**Razón:** Solo reintenta errores **transitorios/recuperables** de red. Los errores de lógica no se solucionan reintentando.

## 🎯 Ventajas del Sistema

1. **Automático** - No requiere intervención manual
2. **Inteligente** - Solo reintenta errores recuperables
3. **Transparente** - Logs claros de cada reintento
4. **Configurable** - Puedes ajustar reintentos y delays
5. **Resiliente** - Maneja problemas transitorios de red

## 🚀 Cómo Probar

### **Test 1: Simulación de Timeout**

1. Reduce temporalmente el timeout:
   ```bash
   SALESFORCE_TIMEOUT=5  # Muy bajo para forzar timeout
   ```

2. Crea un assessment

3. Observa los logs - Deberías ver reintentos

### **Test 2: Conexión Normal**

1. Configuración normal:
   ```bash
   SALESFORCE_TIMEOUT=40
   ```

2. Crea un assessment

3. Debería funcionar en el primer intento (sin reintentos visibles)

## 📈 Monitoreo

### **Métricas Importantes:**

Revisa los logs para:

- **Frecuencia de reintentos** - ¿Cuántas veces se reintenta?
- **Tasa de éxito** - ¿Cuántos reintentos tienen éxito?
- **Tiempo promedio** - ¿Cuánto tarda cada operación?

Si ves muchos reintentos:
1. 🔧 Verifica conexión de internet
2. 🔧 Aumenta `SALESFORCE_TIMEOUT`
3. 🔧 Contacta a Salesforce sobre problemas de servicio

## 🎉 Estado: IMPLEMENTADO

✅ Retry logic implementado en `create_opportunity()`
✅ Retry logic implementado en `get_accounts()`
✅ Exponential backoff configurado
✅ Logs detallados habilitados
✅ Configurable por escenario

**El sistema ahora maneja automáticamente timeouts de Salesforce con reintentos inteligentes.** 🚀
