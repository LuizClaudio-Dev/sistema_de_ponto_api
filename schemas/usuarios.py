from datetime import datetime
from typing import Optional

import brutils
from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuariosBase(BaseModel):
    id_usuario: int = Field(0)
    nome: str = Field('')
    cpf: str = Field('', exclude=True)
    pis: Optional[str] = Field(None, examples=[''])
    email: EmailStr = Field('')
    senha: str = Field('', exclude=True)
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])
    data_criacao: datetime = Field(datetime.now())
    data_atualizacao: Optional[datetime] = Field(
        None, examples=[datetime.now()])

    @field_validator('cpf', mode='after')
    def validar_cpf(cls, value: str):
        if brutils.is_valid_cpf(value):
            return value
        else:
            raise ValueError('CPF inválido!')

    @field_validator('pis', mode='after')
    def validar_pis(cls, value: str):
        if brutils.is_valid_pis(value):
            return value
        else:
            raise ValueError('PIS inválido!')

    class Config:
        from_attributes = True


class GetUsuario(UsuariosBase):
    class Config:
        from_attributes = True
        exclude = {'senha', 'cpf'}


class SetUsuario(UsuariosBase):
    class Config:
        from_attributes = True
        exclude = {'data_criacao', 'data_atualizacao'}
