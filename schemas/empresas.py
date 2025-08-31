from datetime import datetime
from typing import List, Optional

import brutils
from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.common.paginacao import Paginacao


class SetEmpresa(BaseModel):
    model_config = ConfigDict(from_attributes=True,)

    id_empresa: int = Field(0)
    cnpj: str = Field('')
    razao_social: str = Field('')
    nome_fantasia: str = Field('')
    cep: Optional[str] = Field(None, examples=[''])
    logradouro: Optional[str] = Field(None, examples=[''])
    complemento: Optional[str] = Field(None, examples=[''])
    numero: Optional[str] = Field(None, examples=[''])
    bairro: Optional[str] = Field(None, examples=[''])
    cidade: Optional[str] = Field(None, examples=[''])
    uf: Optional[str] = Field(None, examples=[''])
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])

    @field_validator('cnpj')
    def validar_cnpj(cls, value: str):
        if brutils.is_valid_cnpj(value):
            return value
        else:
            raise ValueError('CNPJ inválido!')


class ListEmpresas(BaseModel):
    class Empresa(SetEmpresa):
        data_criacao: datetime = Field(datetime.now())
        data_atualizacao: Optional[datetime] = Field(
            None, examples=[datetime.now()])
    empresas: Optional[List[Empresa]] = Field([], examples=[[Empresa()]])
    paginacao: Optional[Paginacao | dict
                        ] = Field(None, examples=[Paginacao()])
