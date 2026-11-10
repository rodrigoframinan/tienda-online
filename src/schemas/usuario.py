"""Esquemas Pydantic de usuario (Parte 1.1)."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class UsuarioCreate(BaseModel):
    """Datos que envía el cliente para crear un usuario."""

    nombre: str = Field(..., min_length=1, examples=["Ana López"])
    email: str = Field(..., examples=["ana@example.com"])
    tipo: Literal["cliente", "administrador"] = Field("cliente", examples=["cliente"])
    direccion: str | None = Field(None, examples=["Rúa do Príncipe 10, Vigo"])

    @field_validator("email")
    @classmethod
    def email_valido(cls, v: str) -> str:
        v = v.strip()
        usuario, _, dominio = v.partition("@")
        if not usuario or "." not in dominio:
            raise ValueError("El email no tiene un formato válido")
        return v.lower()

    @model_validator(mode="after")
    def cliente_con_direccion(self):
        if self.tipo == "cliente" and not self.direccion:
            raise ValueError("Un cliente necesita dirección postal")
        return self


class UsuarioRead(BaseModel):
    """Datos de usuario que devuelve la API."""

    id: str
    nombre: str
    email: str
    es_admin: bool
