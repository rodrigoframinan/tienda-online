# Tienda Online

**Autor:** Rodrigo Framiñán Rivas
**Asignatura:** Arquitectura del Software — Universidad Intercontinental de la Empresa (UIE)

## Descripción

API REST hecha con **FastAPI** que expone una tienda online (código de la Práctica 2), contenerizada con **Docker** (Práctica 3.2).

- **Usuarios:** clientes (con dirección postal) y administradores.
- **Productos:** clase base `Producto` y especializaciones `ProductoElectronico` (garantía) y `ProductoRopa` (talla y color), con control de stock.
- **Pedidos:** un cliente realiza un pedido de varios productos; se comprueba el stock, se descuenta y se calcula el total.
- **Servicio:** `TiendaService` centraliza el registro de usuarios, el inventario y el histórico de pedidos.
- **Clientes de la API:** documentación interactiva `/docs`, un cliente Python con `requests` y un frontend web.

Los datos se guardan en memoria: al reiniciar el contenedor se pierden.

## Estructura

```text
.
├── Dockerfile              # Imagen de la API (python:3.12-slim)
├── frontend.Dockerfile     # Imagen del frontend (nginx) — extra
├── docker-compose.yml      # Levanta API + frontend — extra
├── .dockerignore           # Ficheros que no entran en la imagen
├── requirements.txt        # Dependencias con versiones fijadas
└── src/
    ├── main.py             # Endpoints FastAPI
    ├── models/             # Producto, Usuario, Pedido
    ├── schemas/            # Esquemas Pydantic de entrada/salida
    ├── services/           # TiendaService (lógica de negocio)
    ├── cliente/cliente.py  # Cliente Python que prueba la API
    └── frontend/index.html # Frontend web
```

## Ejecución sin Docker

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

## Docker

### Dockerfile

| Paso | Instrucción |
| --- | --- |
| Imagen base | `FROM python:3.12-slim` |
| Dependencias | `COPY requirements.txt .` + `RUN pip install -r requirements.txt` (sin caché de pip) |
| Código fuente | `COPY src/ ./src/` |
| Permisos | Se crea el usuario `appuser`, se le da la propiedad de `/app` (`chown`) y el contenedor se ejecuta con `USER appuser`, no como root |
| Inicio | `CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}` |

`requirements.txt` se copia antes que el código para que Docker reutilice la capa de dependencias cuando solo cambia el código.

### Construir la imagen

```bash
docker build -t tienda-online:1.0 -t tienda-online:latest .
docker images tienda-online
```

### Ejecutar el contenedor

```bash
# En primer plano, publicando el puerto 8000
docker run --rm -p 8000:8000 --name tienda tienda-online:1.0

# En segundo plano
docker run -d -p 8000:8000 --name tienda tienda-online:1.0
docker logs -f tienda
docker stop tienda

# Cambiando el puerto interno con la variable PORT
docker run --rm -e PORT=9000 -p 9000:9000 tienda-online:1.0
```

### Variables de entorno

| Variable | Valor por defecto | Descripción |
| --- | --- | --- |
| `PORT` | `8000` | Puerto en el que escucha uvicorn dentro del contenedor |

La aplicación no usa secretos ni claves.

### Salida esperada y pruebas

Al arrancar el contenedor se debe ver:

```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Pruebas:

1. Abrir `http://localhost:8000/docs` en el navegador (documentación interactiva de la API).
2. Probar endpoints con `curl`:
   ```bash
   curl http://localhost:8000/productos          # -> []
   curl -X POST http://localhost:8000/productos \
        -H "Content-Type: application/json" \
        -d '{"tipo":"generico","nombre":"Taza","precio":7.5,"stock":20}'
   curl http://localhost:8000/productos          # -> lista con la taza
   ```
3. Ejecutar el cliente Python contra el contenedor (desde la raíz, con las dependencias instaladas):
   ```bash
   python src/cliente/cliente.py http://localhost:8000
   ```
   Todas las líneas deben salir con `OK` (incluidas las que esperan 400, 404 y 422) y terminar con `Fin de las pruebas.`

Endpoints disponibles:

| Método | Ruta | Respuesta |
| --- | --- | --- |
| POST | `/usuarios` | 201 |
| GET | `/usuarios` | 200 |
| GET | `/usuarios/{usuario_id}` | 200 |
| POST | `/productos` | 201 |
| GET | `/productos` | 200 |
| GET | `/productos/{producto_id}` | 200 |
| DELETE | `/productos/{producto_id}` | 200 |
| POST | `/pedidos` | 201 |
| GET | `/usuarios/{cliente_id}/pedidos` | 200 |

### Publicar la imagen en un registry y descargarla (pull)

Con GitHub Container Registry (hace falta un token de GitHub con permiso `write:packages`, que **no** se sube al repositorio):

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u rodrigoframinan --password-stdin
docker tag tienda-online:1.0 ghcr.io/rodrigoframinan/tienda-online:1.0
docker push ghcr.io/rodrigoframinan/tienda-online:1.0
```

Descargar y ejecutar la imagen publicada en cualquier equipo:

```bash
docker pull ghcr.io/rodrigoframinan/tienda-online:1.0
docker run --rm -p 8000:8000 ghcr.io/rodrigoframinan/tienda-online:1.0
```

(Con Docker Hub es igual cambiando `ghcr.io/rodrigoframinan` por `<usuario-dockerhub>` y haciendo `docker login`.)

### Extra: API + frontend con docker-compose

`frontend.Dockerfile` sirve `src/frontend/index.html` con nginx, y `docker-compose.yml` levanta los dos contenedores:

```bash
docker compose up --build -d
```

- API: `http://localhost:8000/docs`
- Frontend: `http://localhost:8080` (el campo de la dirección de la API ya apunta a `http://localhost:8000`)

```bash
docker compose down
```

## Flujo de trabajo Git

- `main`: rama principal y estable.
- `feature/<nombre>`: una rama por funcionalidad, que se integra en `main` mediante Pull Request (`feature/docker` para esta práctica).
