from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class GetUsuario(BaseModel):
    id_usuario: int = Field(0)
    nome: str = Field('')
    cpf: str = Field('', exclude=True)
    email: EmailStr = Field('')
    senha: str = Field('', exclude=True)
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])
    data_criacao: datetime = Field(datetime.now())
    data_atualizacao: Optional[datetime] = Field(
        None, examples=[datetime.now()])

    class Config:
        from_attributes = True


class SetUsuario(BaseModel):
    id_usuario: int = Field(0)
    nome: str = Field('')
    cpf: str = Field('')
    email: EmailStr = Field('')
    senha: str = Field('')
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])

    class Config:
        from_attributes = True
