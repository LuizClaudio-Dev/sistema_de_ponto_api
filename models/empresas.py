from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GetEmpresa(BaseModel):
    id_empresa: int = Field(0)
    cnpj: str = Field('')
    razao_social: str = Field('')
    nome_fantasia: str = Field('')
    cep: Optional[str] = Field(None, examples=[''])
    logradouro: Optional[str] = Field(None, examples=[''])
    numero: Optional[str] = Field(None, examples=[''])
    bairro: Optional[str] = Field(None, examples=[''])
    cidade: Optional[str] = Field(None, examples=[''])
    uf: Optional[str] = Field(None, examples=[''])
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])
    data_criacao: datetime = Field('')
    data_atualizacao: datetime = Field('')

    class Config:
        from_attributes = True


class SetEmpresa(BaseModel):
    id_empresa: int = Field(0)
    cnpj: str = Field('')
    razao_social: str = Field('')
    nome_fantasia: str = Field('')
    cep: Optional[str] = Field(None, examples=[''])
    logradouro: Optional[str] = Field(None, examples=[''])
    numero: Optional[str] = Field(None, examples=[''])
    bairro: Optional[str] = Field(None, examples=[''])
    cidade: Optional[str] = Field(None, examples=[''])
    uf: Optional[str] = Field(None, examples=[''])
    ativo: int = Field(1)
    motivo: Optional[str] = Field(None, examples=[''])

    class Config:
        from_attributes = True
