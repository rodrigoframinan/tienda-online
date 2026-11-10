# a. Imagen base ligera de Python
FROM python:3.12-slim

# Evita ficheros .pyc, fuerza salida sin buffer y no guarda caché de pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

WORKDIR /app

# b. Copia solo las dependencias primero (aprovecha la caché de capas de Docker)
COPY requirements.txt .

# c. Instala las dependencias con versiones fijadas
RUN pip install -r requirements.txt

# Usuario sin privilegios para no ejecutar la app como root
RUN useradd --create-home --uid 1000 appuser

# d. Copia el código fuente
COPY src/ ./src/

# e. Cambia los permisos para que el usuario pueda leer y ejecutar el código
RUN chown -R appuser:appuser /app && chmod -R u+rwX /app

USER appuser
WORKDIR /app/src

EXPOSE 8000

# f. Comando de inicio: arranca la API escuchando en todas las interfaces
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
