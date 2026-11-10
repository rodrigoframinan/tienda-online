import uuid


class Usuario:
    """Usuario de la tienda."""

    def __init__(self, nombre: str, email: str):
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Devuelve si el usuario es administrador."""
        return False


class Cliente(Usuario):
    """Cliente con dirección postal."""

    def __init__(self, nombre: str, email: str, direccion: str):
        super().__init__(nombre, email)
        self.direccion: str = direccion


class Administrador(Usuario):
    """Administrador de la tienda."""

    def is_admin(self) -> bool:
        """Devuelve True porque es administrador."""
        return True
