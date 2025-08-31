# type: ignore
import datetime
from typing import List, Optional

from sqlalchemy import (SMALLINT, TIMESTAMP, Integer, PrimaryKeyConstraint,
                        String, Text, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Empresas(Base):
    __tablename__ = "empresas"
    __table_args__ = (
        PrimaryKeyConstraint("id_empresa", name="empresas_pkey"),
    )

    id_empresa: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    cnpj: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    razao_social: Mapped[str] = mapped_column(String(100), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(String(100), nullable=False)
    cep: Mapped[Optional[str]] = mapped_column(String(8))
    logradouro: Mapped[Optional[str]] = mapped_column(String(100))
    complemento: Mapped[Optional[str]] = mapped_column(String(100))
    numero: Mapped[Optional[str]] = mapped_column(String(10))
    bairro: Mapped[Optional[str]] = mapped_column(String(100))
    cidade: Mapped[Optional[str]] = mapped_column(String(100))
    uf: Mapped[Optional[str]] = mapped_column(String(2))
    ativo: Mapped[int] = mapped_column(
        DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
               not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True, onupdate=text("CURRENT_TIMESTAMP"))
