"""Punto de entrada de la API REST de la tienda online.

main.py es la capa de exposición: define los endpoints, recibe las peticiones
HTTP, llama a TiendaService (la lógica de la Práctica 1) y devuelve la
respuesta con el código HTTP adecuado.

Ejecutar:
    uvicorn main:app --reload                     (solo este equipo)
    uvicorn main:app --host 0.0.0.0 --port 8000   (accesible desde la red)
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models.Producto import Producto, ProductoElectronico, ProductoRopa
from schemas import (
    PedidoCreate, PedidoItemRead, PedidoRead,
    ProductoCreate, ProductoRead, UsuarioCreate, UsuarioRead,
)
from services.Tienda_service import (
    EmailDuplicadoError, NoEncontradoError, OperacionNoValidaError, TiendaService,
)

app = FastAPI(
    title="Tienda online",
    description="API REST de la tienda online (Práctica 2)",
    version="1.0",
)

# Permite que el frontend (abierto en el navegador desde otro origen, p. ej.
# un fichero local o otro puerto) pueda llamar a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Una única instancia del servicio para toda la aplicación (datos en memoria)
tienda = TiendaService()


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def error_http(e: Exception) -> HTTPException:
    """Traduce los errores de TiendaService a códigos HTTP."""
    if isinstance(e, NoEncontradoError):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    if isinstance(e, EmailDuplicadoError):
        return HTTPException(status.HTTP_409_CONFLICT, detail=str(e))
    return HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


ERRORES_TIENDA = (NoEncontradoError, EmailDuplicadoError, OperacionNoValidaError)


def a_usuario_read(u) -> UsuarioRead:
    """Convierte un objeto Usuario en el esquema de salida."""
    return UsuarioRead(id=u.id, nombre=u.nombre, email=u.email, es_admin=u.is_admin())


def a_producto_read(p) -> ProductoRead:
    """Convierte un objeto Producto en el esquema de salida.
    El tipo se deduce de la clase del objeto."""
    if isinstance(p, ProductoElectronico):
        return ProductoRead(id=p.id, tipo="electronico", nombre=p.nombre, precio=p.precio,
                            stock=p.stock, meses_garantia=p.garantia)
    if isinstance(p, ProductoRopa):
        return ProductoRead(id=p.id, tipo="ropa", nombre=p.nombre, precio=p.precio,
                            stock=p.stock, talla=p.talla, color=p.color)
    return ProductoRead(id=p.id, tipo="generico", nombre=p.nombre, precio=p.precio, stock=p.stock)


def a_pedido_read(pedido) -> PedidoRead:
    """Convierte un objeto Pedido en el esquema de salida."""
    items = []
    for producto, cantidad in pedido.productos:
        items.append(PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            subtotal=round(producto.precio * cantidad, 2),
        ))
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        total=pedido.calcular_total(),
        items=items,
    )


@app.get("/", tags=["General"])
def inicio():
    return {"mensaje": "API de la tienda online. Documentación en /docs"}


# ---------------------------------------------------------------------------
# Usuarios
# ---------------------------------------------------------------------------
@app.post("/usuarios", response_model=UsuarioRead,
          status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(datos: UsuarioCreate):
    try:
        usuario = tienda.registrar_usuario(datos.tipo, datos.nombre, datos.email,
                                           datos.direccion or "")
    except ERRORES_TIENDA as e:
        raise error_http(e)
    return a_usuario_read(usuario)


@app.get("/usuarios", response_model=list[UsuarioRead], tags=["Usuarios"])
def listar_usuarios():
    return [a_usuario_read(u) for u in tienda.listar_usuarios()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: str):
    try:
        return a_usuario_read(tienda.obtener_usuario(usuario_id))
    except ERRORES_TIENDA as e:
        raise error_http(e)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead],
         tags=["Pedidos"])
def pedidos_de_cliente(cliente_id: str):
    try:
        return [a_pedido_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]
    except ERRORES_TIENDA as e:
        raise error_http(e)


# ---------------------------------------------------------------------------
# Productos
# ---------------------------------------------------------------------------
@app.post("/productos", response_model=ProductoRead,
          status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(datos: ProductoCreate):
    # Se crea el objeto de la clase que corresponde al tipo.
    # Pydantic ya ha comprobado que vienen los campos necesarios de cada tipo.
    if datos.tipo == "electronico":
        producto = ProductoElectronico(datos.nombre, datos.precio, datos.stock,
                                       datos.meses_garantia)
    elif datos.tipo == "ropa":
        producto = ProductoRopa(datos.nombre, datos.precio, datos.stock,
                                datos.talla, datos.color)
    else:
        producto = Producto(datos.nombre, datos.precio, datos.stock)

    tienda.anadir_producto(producto)
    return a_producto_read(producto)


@app.get("/productos", response_model=list[ProductoRead], tags=["Productos"])
def listar_productos():
    return [a_producto_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: str):
    try:
        return a_producto_read(tienda.obtener_producto(producto_id))
    except ERRORES_TIENDA as e:
        raise error_http(e)


@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: str):
    try:
        tienda.eliminar_producto(producto_id)
    except ERRORES_TIENDA as e:
        raise error_http(e)
    return {"mensaje": f"Producto {producto_id} eliminado"}


# ---------------------------------------------------------------------------
# Pedidos
# ---------------------------------------------------------------------------
@app.post("/pedidos", response_model=PedidoRead,
          status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(datos: PedidoCreate):
    try:
        # TiendaService.realizar_pedido trabaja con objetos (producto, cantidad),
        # así que primero se busca cada producto por su id (404 si no existe).
        lineas = [(tienda.obtener_producto(item.producto_id), item.cantidad)
                  for item in datos.items]
        pedido = tienda.realizar_pedido(datos.cliente_id, lineas)
    except ERRORES_TIENDA as e:
        raise error_http(e)
    return a_pedido_read(pedido)
