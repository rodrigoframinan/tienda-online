"""Cliente Python de la API de la tienda (Práctica 2, parte 2 - Parte 1).

Este script NO importa nada del servidor (ni TiendaService ni los modelos):
todo se hace con peticiones HTTP usando la librería requests.

Uso:
    python cliente.py                              -> usa BASE_URL de abajo
    python cliente.py http://192.168.1.34:8000     -> usa la IP indicada
"""

import sys
import time

import requests

# Dirección de la API. Cambiarla aquí o pasarla como argumento.
BASE_URL = "http://localhost:8000"
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1].rstrip("/")


def comprobar(respuesta: requests.Response, esperado: int, accion: str):
    """Comprueba el código HTTP y devuelve el JSON de la respuesta."""
    datos = respuesta.json()
    if respuesta.status_code == esperado:
        print(f"  OK  {respuesta.status_code}  {accion}")
    else:
        print(f"  ERROR {respuesta.status_code} (esperado {esperado})  {accion}")
        print(f"        Detalle: {datos.get('detail') if isinstance(datos, dict) else datos}")
    return datos


def main():
    print(f"Conectando con la API en {BASE_URL}\n")
    try:
        requests.get(BASE_URL, timeout=5)
    except requests.ConnectionError:
        print("No se puede conectar. ¿Está el servidor arrancado y la IP es correcta?")
        sys.exit(1)

    # Email distinto en cada ejecución para no chocar con el de una ejecución anterior
    sufijo = int(time.time())

    # 1. Crear un usuario
    print("1. Crear usuario")
    r = requests.post(f"{BASE_URL}/usuarios", json={
        "nombre": "Ana López",
        "email": f"ana{sufijo}@example.com",
        "tipo": "cliente",
        "direccion": "Rúa do Príncipe 10, Vigo",
    })
    usuario = comprobar(r, 201, "POST /usuarios")
    print(f"     Creado: {usuario['nombre']}, admin={usuario['es_admin']}, id={usuario['id']}")

    # 2. Consultar la lista de usuarios
    print("\n2. Listar usuarios")
    usuarios = comprobar(requests.get(f"{BASE_URL}/usuarios"), 200, "GET /usuarios")
    for u in usuarios:
        print(f"     {u['nombre']} <{u['email']}>  id={u['id']}")

    # 3. Crear varios productos (uno de cada tipo)
    print("\n3. Crear productos")
    nuevos = [
        {"tipo": "generico", "nombre": "Taza", "precio": 7.5, "stock": 20},
        {"tipo": "electronico", "nombre": "Auriculares", "precio": 59.9,
         "stock": 5, "meses_garantia": 24},
        {"tipo": "ropa", "nombre": "Camiseta", "precio": 15.0, "stock": 10,
         "talla": "M", "color": "azul"},
    ]
    ids = []
    for p in nuevos:
        creado = comprobar(requests.post(f"{BASE_URL}/productos", json=p),
                           201, f"POST /productos ({p['nombre']})")
        ids.append(creado["id"])

    # Prueba de validación: ropa sin talla -> la API debe responder 422
    r = requests.post(f"{BASE_URL}/productos",
                      json={"tipo": "ropa", "nombre": "Pantalón", "precio": 30, "stock": 3})
    comprobar(r, 422, "POST /productos (ropa sin talla, debe fallar)")

    # 4. Consultar la lista de productos
    print("\n4. Listar productos")
    productos = comprobar(requests.get(f"{BASE_URL}/productos"), 200, "GET /productos")
    for p in productos:
        print(f"     {p['nombre']} ({p['tipo']}) {p['precio']} € - stock {p['stock']}")

    # 5. Crear un pedido para el usuario
    print("\n5. Crear pedido")
    r = requests.post(f"{BASE_URL}/pedidos", json={
        "cliente_id": usuario["id"],
        "items": [
            {"producto_id": ids[0], "cantidad": 2},
            {"producto_id": ids[1], "cantidad": 1},
        ],
    })
    pedido = comprobar(r, 201, "POST /pedidos")
    print(f"     Pedido creado - total {pedido['total']} €")

    # Prueba de error: pedir más stock del que hay -> 400
    r = requests.post(f"{BASE_URL}/pedidos", json={
        "cliente_id": usuario["id"],
        "items": [{"producto_id": ids[1], "cantidad": 999}],
    })
    comprobar(r, 400, "POST /pedidos (sin stock suficiente, debe fallar)")

    # 6. Consultar los pedidos del usuario
    print("\n6. Pedidos del usuario")
    pedidos = comprobar(requests.get(f"{BASE_URL}/usuarios/{usuario['id']}/pedidos"),
                        200, f"GET /usuarios/{usuario['id']}/pedidos")
    for p in pedidos:
        print(f"     Pedido del {p['fecha'][:16]} - total {p['total']} €")
        for linea in p["items"]:
            print(f"        {linea['cantidad']} x {linea['nombre']} = {linea['subtotal']} €")

    # Prueba de error: usuario que no existe -> 404
    comprobar(requests.get(f"{BASE_URL}/usuarios/id-inventado"), 404,
              "GET /usuarios/id-inventado (no existe, debe fallar)")

    print("\nFin de las pruebas.")


if __name__ == "__main__":
    main()
