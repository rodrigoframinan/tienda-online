import uuid


class Producto:
    """Producto de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int):
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Comprueba si hay stock suficiente."""
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int):
        """Suma unidades al stock (se pasa en negativo para restar)."""
        self.stock = self.stock + cantidad

    def __str__(self) -> str:
        return f"{self.nombre} | Precio: {self.precio} € | Stock: {self.stock}"


class ProductoElectronico(Producto):
    """Producto electrónico con garantía."""

    def __init__(self, nombre: str, precio: float, stock: int, garantia: int):
        super().__init__(nombre, precio, stock)
        self.garantia: int = garantia

    def __str__(self) -> str:
        return f"{self.nombre} | Precio: {self.precio} € | Stock: {self.stock} | Garantía: {self.garantia} meses"


class ProductoRopa(Producto):
    """Producto de ropa con talla y color."""

    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        return f"{self.nombre} | Precio: {self.precio} € | Stock: {self.stock} | Talla: {self.talla} | Color: {self.color}"
