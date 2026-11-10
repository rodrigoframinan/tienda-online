from models.Pedido import Pedido
from models.Usuario import Cliente, Administrador


# ---------------------------------------------------------------------------
# Cambio respecto a la Práctica 1: antes, cuando algo fallaba, se hacía un
# print() y se devolvía None. Una API necesita saber QUÉ ha fallado para
# responder con el código HTTP correcto, así que ahora se lanzan estos errores.
# main.py los recoge y los convierte en 404, 400 o 409.
# ---------------------------------------------------------------------------
class NoEncontradoError(Exception):
    """El usuario o el producto no existe (-> 404)."""


class OperacionNoValidaError(Exception):
    """La operación no se puede hacer, p. ej. falta stock (-> 400)."""


class EmailDuplicadoError(Exception):
    """Ya hay un usuario con ese email (-> 409)."""


class TiendaService:
    """Gestiona los usuarios, productos y pedidos de la tienda."""

    def __init__(self):
        self.usuarios: dict = {}
        self.productos: dict = {}
        self.pedidos: list = []

    # ---------------- Usuarios ----------------
    def registrar_usuario(self, tipo: str, nombre: str, email: str, direccion: str = ""):
        """Registra un cliente o un administrador."""
        # Nuevo: no se permiten dos usuarios con el mismo email
        for usuario in self.usuarios.values():
            if usuario.email.lower() == email.lower():
                raise EmailDuplicadoError(f"Ya existe un usuario con el email {email}")

        if tipo == "cliente":
            usuario = Cliente(nombre, email, direccion)
        else:
            usuario = Administrador(nombre, email)
        self.usuarios[usuario.id] = usuario
        return usuario

    def listar_usuarios(self) -> list:
        """Nuevo: devuelve la lista de usuarios."""
        return list(self.usuarios.values())

    def obtener_usuario(self, usuario_id: str):
        """Nuevo: devuelve un usuario por su id."""
        if usuario_id not in self.usuarios:
            raise NoEncontradoError(f"El usuario {usuario_id} no existe")
        return self.usuarios[usuario_id]

    # ---------------- Productos ----------------
    def anadir_producto(self, producto):
        """Añade un producto al inventario."""
        self.productos[producto.id] = producto

    def eliminar_producto(self, producto_id: str):
        """Elimina un producto por su id."""
        if producto_id not in self.productos:
            raise NoEncontradoError(f"El producto {producto_id} no existe")
        del self.productos[producto_id]

    def listar_productos(self) -> list:
        """Devuelve la lista de productos."""
        return list(self.productos.values())

    def obtener_producto(self, producto_id: str):
        """Nuevo: devuelve un producto por su id."""
        if producto_id not in self.productos:
            raise NoEncontradoError(f"El producto {producto_id} no existe")
        return self.productos[producto_id]

    # ---------------- Pedidos ----------------
    def realizar_pedido(self, usuario_id: str, productos: list):
        """Crea un pedido si el usuario existe y hay stock. productos es una lista de (producto, cantidad)."""
        usuario = self.obtener_usuario(usuario_id)  # lanza NoEncontradoError si no existe

        if not isinstance(usuario, Cliente):
            raise OperacionNoValidaError("Solo los clientes pueden hacer pedidos")

        # Se suman las cantidades por producto, por si el mismo producto
        # aparece en varias líneas del pedido
        necesario = {}
        for producto, cantidad in productos:
            necesario[producto.id] = necesario.get(producto.id, 0) + cantidad

        for producto, cantidad in productos:
            if not producto.hay_stock(necesario[producto.id]):
                raise OperacionNoValidaError(
                    f"No hay stock suficiente de {producto.nombre} "
                    f"(pedidas {necesario[producto.id]}, disponibles {producto.stock})")

        for producto, cantidad in productos:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(usuario, productos)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> list:
        """Devuelve los pedidos de un usuario ordenados por fecha."""
        self.obtener_usuario(usuario_id)  # nuevo: error 404 si el usuario no existe
        resultado = []
        for pedido in self.pedidos:
            if pedido.cliente.id == usuario_id:
                resultado.append(pedido)
        resultado.sort(key=lambda pedido: pedido.fecha)
        return resultado
