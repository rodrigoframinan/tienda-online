"""Esquemas Pydantic de pedido (Parte 1.3)."""

from datetime import datetime

from pydantic import BaseModel, Field


class PedidoItemCreate(BaseModel):
    """Una línea al crear un pedido: qué producto y cuántas unidades."""

    producto_id: str = Field(..., examples=["id-del-producto"])
    cantidad: int = Field(..., gt=0, examples=[2])


class PedidoCreate(BaseModel):
    """Datos para crear un pedido."""

    cliente_id: str = Field(..., examples=["id-del-cliente"])
    items: list[PedidoItemCreate] = Field(..., min_length=1)


class PedidoItemRead(BaseModel):
    """Una línea de pedido tal y como la devuelve la API."""

    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRead(BaseModel):
    """Pedido completo que devuelve la API."""

    id: str
    fecha: datetime
    cliente_id: str
    total: float
    items: list[PedidoItemRead]
