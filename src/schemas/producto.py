"""Esquemas Pydantic de producto (Parte 1.2)."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

TipoProducto = Literal["generico", "electronico", "ropa"]


class ProductoCreate(BaseModel):
    """Datos para crear un producto.

    Según el tipo se exigen campos extra:
    - electronico -> meses_garantia
    - ropa        -> talla y color
    """

    tipo: TipoProducto = Field("generico", examples=["electronico"])
    nombre: str = Field(..., min_length=1, examples=["Auriculares"])
    precio: float = Field(..., ge=0, examples=[59.9])
    stock: int = Field(..., ge=0, examples=[10])
    meses_garantia: int | None = Field(None, ge=0, examples=[24])
    talla: str | None = Field(None, examples=[None])
    color: str | None = Field(None, examples=[None])

    @model_validator(mode="after")
    def campos_segun_tipo(self):
        if self.tipo == "electronico" and self.meses_garantia is None:
            raise ValueError("Un producto electrónico necesita meses_garantia")
        if self.tipo == "ropa" and (not self.talla or not self.color):
            raise ValueError("Un producto de ropa necesita talla y color")
        return self


class ProductoRead(BaseModel):
    """Producto que devuelve la API. Los campos extra solo vienen rellenos
    si corresponden a su tipo."""

    id: str
    tipo: TipoProducto
    nombre: str
    precio: float
    stock: int
    meses_garantia: int | None = None
    talla: str | None = None
    color: str | None = None
