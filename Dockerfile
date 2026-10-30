# Imagen ligera de Python
FROM python:3.12-slim

# Evita ficheros .pyc y fuerza salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copia el código de la aplicación
COPY . .

# Ejecuta la demo de la tienda
CMD ["python", "main.py"]
