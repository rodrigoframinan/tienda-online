# Tienda Online

**Autor:** Rodrigo Framiñán Rivas
**Asignatura:** Arquitectura del Software — Universidad Intercontinental de la Empresa (UIE)

## Descripción

Aplicación de consola en Python que simula una tienda online siguiendo los principios de la Programación Orientada a Objetos (código de la Práctica 1.3).

- **Usuarios:** clientes (con dirección postal) y administradores.
- **Productos:** clase base `Producto` y especializaciones `ProductoElectronico` (garantía) y `ProductoRopa` (talla y color), con control de stock.
- **Pedidos:** un cliente realiza un pedido de varios productos; se comprueba el stock, se descuenta y se calcula el total.
- **Servicio:** `TiendaService` centraliza el registro de usuarios, el inventario y el histórico de pedidos.

Este repositorio se usará también en las prácticas 3.2 y 3.3.

## Estructura

```
.
├── main.py                 # Punto de entrada: demo de la tienda
├── models/
│   ├── Usuario.py          # Usuario, Cliente, Administrador
│   ├── Producto.py         # Producto, ProductoElectronico, ProductoRopa
│   └── Pedido.py           # Pedido
└── services/
    └── Tienda_service.py   # Lógica de negocio de la tienda
```

## Ejecución

Requiere Python 3.10 o superior (sin dependencias externas).

```bash
python3 main.py
```

## Flujo de trabajo Git

- `main`: rama principal y estable.
- `feature/<nombre>`: una rama por funcionalidad, que se integra en `main` mediante Pull Request.

## Ejecución con Docker

```bash
docker build -t tienda-online .
docker run --rm tienda-online
```
