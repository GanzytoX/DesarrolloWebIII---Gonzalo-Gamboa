# Imagen base ligera de Python
# FROM mirror.gcr.io/library/python:3.11-slim
FROM python:3.11-slim
# FROM gcr.io/google-containers/python:3.5.1-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación con Uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]