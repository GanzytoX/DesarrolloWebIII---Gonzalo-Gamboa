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

## 🏗️ Arquitectura

- **Frontend**: React (Puerto 3000)
- **Backend**: FastAPI (Puerto 8089)
- **Base de datos**: MongoDB (Puerto 27020)
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
├── backend/
│   ├── main.py
│   ├── test_main.py
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/App.js
    ├── package.json
    └── Dockerfile
```

## 🔧 Solución de Problemas

| Problema                | Solución                            |
| ----------------------- | ----------------------------------- |
| Puerto ocupado          | `docker-compose down -v`            |
| Cambios no se reflejan  | `docker-compose restart calculator` |
| Contenedores no inician | Verificar Docker Desktop activo     |
| Errores de conexión     | `docker-compose logs mongo`         |

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
