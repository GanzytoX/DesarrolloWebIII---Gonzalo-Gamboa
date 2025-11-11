# Calculadora con Docker - Desarrollo Web III

Calculadora web que soporta operaciones con múltiples números (2 o más), desarrollada con FastAPI, React y MongoDB.

## 🚀 Inicio Rápido

```bash
# 1. Clonar y navegar al directorio
cd "C:\dev\Tareas\Desarrollo Web III"

# 2. Levantar los contenedores
docker-compose up --build

# 3. Acceder a la aplicación
# Frontend: http://localhost:3000
# API Docs: http://localhost:8089/docs
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
# Métricas API: http://localhost:8089/metrics
```

## 🛠️ Comandos Útiles

```bash
# Detener contenedores
docker-compose down

# Reiniciar contenedores
docker-compose restart

# Ver logs
docker-compose logs

# Ejecutar pruebas
docker-compose exec calculator python -m pytest test_main.py -v
```

## 📡 Endpoints API

### Operaciones Básicas

```bash
# Suma múltiple
curl "http://localhost:8089/calculator/sum?numbers=5&numbers=10&numbers=15"

# Resta múltiple
curl "http://localhost:8089/calculator/substract?numbers=20&numbers=5&numbers=3"

# Multiplicación múltiple
curl "http://localhost:8089/calculator/multiply?numbers=2&numbers=3&numbers=4"

# División múltiple
curl "http://localhost:8089/calculator/divide?numbers=100&numbers=2&numbers=5"

# Historial
curl "http://localhost:8089/calculator/history"
```

### Casos de Error

```bash
# Números insuficientes
curl "http://localhost:8089/calculator/sum?numbers=5"

# Números negativos
curl "http://localhost:8089/calculator/sum?numbers=-5&numbers=10"

# División por cero
curl "http://localhost:8089/calculator/divide?numbers=10&numbers=0"
```

## ✨ Características

- ✅ **Operaciones con N números** (suma, resta, multiplicación, división)
- ✅ **Validaciones robustas** (números negativos, división por cero)
- ✅ **Historial con filtros** por operación y fecha
- ✅ **API documentada** con Swagger UI
- ✅ **Tests unitarios** (29 tests, 69% cobertura)
- ✅ **Monitoreo con Prometheus** y Grafana
- ✅ **Logs centralizados** con Loki y Promtail
- ✅ **Métricas HTTP** automáticas

## 🏗️ Arquitectura

- **Frontend**: React (Puerto 3000)
- **Backend**: FastAPI (Puerto 8089)
- **Base de datos**: MongoDB (Puerto 27017)
- **Prometheus**: Métricas (Puerto 9090)
- **Grafana**: Dashboards (Puerto 3001)
- **Loki**: Logs centralizados (Puerto 3100)
- **Promtail**: Recolector de logs
- **Contenedores**: Docker Compose

## 🧪 Testing

```bash
# Todas las pruebas
docker-compose exec calculator python -m pytest test_main.py -v

# Con cobertura
docker-compose exec calculator python -m pytest test_main.py --cov=main --cov-report=term-missing

# Resultado esperado: 29 passed
```

## 📋 Estructura del Proyecto

```
proyecto/
├── docker-compose.yml
├── .env                      # Variables de entorno
├── backend/
│   ├── main.py              # API FastAPI
│   ├── logging.py           # Configuración de logs
│   ├── test_main.py         # Tests unitarios
│   ├── requirements.txt     # Dependencias Python
│   └── Dockerfile
├── frontend/
│   ├── src/App.js
│   ├── package.json
│   └── Dockerfile
└── monitoring/
    ├── prometheus.yml       # Configuración Prometheus
    ├── loki-config.yaml     # Configuración Loki
    └── promtail-config.yaml # Configuración Promtail
```

## � Monitoreo y Observabilidad

### Prometheus (http://localhost:9090)

Métricas de rendimiento de la API:

- Número de requests HTTP
- Latencia de respuestas
- Códigos de estado HTTP
- Métricas personalizadas

### Grafana (http://localhost:3001)

Dashboards de visualización:

- **Usuario**: admin
- **Contraseña**: admin
- Crear dashboards desde Prometheus datasource
- Visualizar logs desde Loki datasource

### Loki + Promtail

Sistema de logs centralizados:

- Logs de todos los contenedores
- Búsqueda y filtrado avanzado
- Integración con Grafana
- Retención de 7 días

### Métricas API (http://localhost:8089/metrics)

Endpoint de Prometheus con métricas detalladas en formato estándar.

### Configuración de Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
# MongoDB
MONGO_INITDB_ROOT_USERNAME=admin_user
MONGO_INITDB_ROOT_PASSWORD=web3

# GitHub Container Registry
GHCR_OWNER=tu-usuario-github
GHCR_REPO=tu-repo

# Tags de imágenes
BACKEND_TAG=latest
FRONTEND_TAG=latest

# Nivel de logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

## �🔧 Solución de Problemas

| Problema                 | Solución                               |
| ------------------------ | -------------------------------------- |
| Puerto ocupado           | `docker-compose down -v`               |
| Cambios no se reflejan   | `docker-compose restart calculadora`   |
| Contenedores no inician  | Verificar Docker Desktop activo        |
| Errores de conexión      | `docker-compose logs mongo`            |
| Logs no aparecen en Loki | `docker-compose logs loki promtail`    |
| Prometheus sin datos     | Verificar endpoint `/metrics` funciona |
| Grafana no conecta       | Revisar datasources en configuración   |

## 📊 Respuestas API

**Operación exitosa:**

```json
{
  "numbers": [10.0, 20.0, 30.0],
  "result": 60.0
}
```

**Error de validación:**

```json
{
  "error": "Negative numbers are not allowed",
  "operation": "sum",
  "operands": [-5.0, 10.0]
}
```

---

**Desarrollo Web III** - Versión 1.0
