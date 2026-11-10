import uuid
from datetime import datetime


class Pedido:
    """Pedido de un cliente. productos es una lista de (producto, cantidad)."""

    def __init__(self, cliente, productos: list):
        self.id: str = str(uuid.uuid4())
        self.cliente = cliente
        self.productos: list = productos
        self.fecha: datetime = datetime.now()

    def calcular_total(self) -> float:
        """Calcula el total del pedido."""
        total = 0
        for producto, cantidad in self.productos:
            total = total + producto.precio * cantidad
        return round(total, 2)

    def __str__(self) -> str:
        return f"Pedido de {self.cliente.nombre} | Fecha: {self.fecha} | Total: {self.calcular_total()} €"
