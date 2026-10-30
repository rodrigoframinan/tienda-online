from models.Pedido import Pedido
from models.Usuario import Cliente, Administrador


class TiendaService:
    """Gestiona los usuarios, productos y pedidos de la tienda."""

    def __init__(self):
        self.usuarios: dict = {}
        self.productos: dict = {}
        self.pedidos: list = []

    def registrar_usuario(self, tipo: str, nombre: str, email: str, direccion: str = ""):
        """Registra un cliente o un administrador."""
        if tipo == "cliente":
            usuario = Cliente(nombre, email, direccion)
        else:
            usuario = Administrador(nombre, email)
        self.usuarios[usuario.id] = usuario
        return usuario

    def anadir_producto(self, producto):
        """Añade un producto al inventario."""
        self.productos[producto.id] = producto

    def eliminar_producto(self, producto_id: str):
        """Elimina un producto por su id."""
        if producto_id in self.productos:
            del self.productos[producto_id]

    def listar_productos(self) -> list:
        """Devuelve la lista de productos."""
        return list(self.productos.values())

    def realizar_pedido(self, usuario_id: str, productos: list):
        """Crea un pedido si el usuario existe y hay stock. productos es una lista de (producto, cantidad)."""
        if usuario_id not in self.usuarios:
            print("El usuario no existe")
            return None

        for producto, cantidad in productos:
            if not producto.hay_stock(cantidad):
                print(f"No hay stock suficiente de {producto.nombre}")
                return None

        for producto, cantidad in productos:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(self.usuarios[usuario_id], productos)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> list:
        """Devuelve los pedidos de un usuario ordenados por fecha."""
        resultado = []
        for pedido in self.pedidos:
            if pedido.cliente.id == usuario_id:
                resultado.append(pedido)
        resultado.sort(key=lambda pedido: pedido.fecha)
        return resultado
