from models.Producto import ProductoElectronico, ProductoRopa
from services.Tienda_service import TiendaService


def main():
    """Prueba la tienda."""
    tienda = TiendaService()

    ana = tienda.registrar_usuario("cliente", "Ana", "ana@mail.com", "Calle Mayor 1, Vigo")
    luis = tienda.registrar_usuario("cliente", "Luis", "luis@mail.com", "Rúa Nova 5, Santiago")
    marta = tienda.registrar_usuario("cliente", "Marta", "marta@mail.com", "Avenida Galicia 10, A Coruña")
    admin = tienda.registrar_usuario("administrador", "Admin", "admin@mail.com")

    portatil = ProductoElectronico("Portátil", 900, 10, 24)
    movil = ProductoElectronico("Móvil", 500, 15, 12)
    auriculares = ProductoElectronico("Auriculares", 60, 30, 6)
    camiseta = ProductoRopa("Camiseta", 20, 50, "M", "Blanco")
    pantalon = ProductoRopa("Pantalón", 40, 20, "L", "Azul")

    tienda.anadir_producto(portatil)
    tienda.anadir_producto(movil)
    tienda.anadir_producto(auriculares)
    tienda.anadir_producto(camiseta)
    tienda.anadir_producto(pantalon)

    print("PRODUCTOS")
    for producto in tienda.listar_productos():
        print(producto)

    print("\nPEDIDOS")
    pedido1 = tienda.realizar_pedido(ana.id, [(portatil, 1), (auriculares, 2)])
    print(pedido1)
    pedido2 = tienda.realizar_pedido(luis.id, [(camiseta, 3), (pantalon, 1)])
    print(pedido2)
    pedido3 = tienda.realizar_pedido(marta.id, [(movil, 1), (camiseta, 2)])
    print(pedido3)
    pedido4 = tienda.realizar_pedido(ana.id, [(pantalon, 2)])
    print(pedido4)

    print("\nHISTÓRICO DE ANA")
    for pedido in tienda.listar_pedidos_usuario(ana.id):
        print(pedido)

    print("\nSTOCK ACTUALIZADO")
    for producto in tienda.listar_productos():
        print(producto)


if __name__ == "__main__":
    main()
