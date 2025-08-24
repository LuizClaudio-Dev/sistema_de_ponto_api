# type: ignore
import datetime
from typing import List, Optional

from sqlalchemy import SMALLINT, TIMESTAMP, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Empresas(Base):
    __tablename__ = "empresas"

    id_empresa: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    cnpj: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    razao_social: Mapped[str] = mapped_column(String(100), nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(String(100), nullable=False)
    cep: Mapped[Optional[str]] = mapped_column(String(8))
    logradouro: Mapped[Optional[str]] = mapped_column(String(100))
    numero: Mapped[Optional[str]] = mapped_column(String(10))
    bairro: Mapped[Optional[str]] = mapped_column(String(100))
    cidade: Mapped[Optional[str]] = mapped_column(String(100))
    uf: Mapped[Optional[str]] = mapped_column(String(2))
    ativo: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1)
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()"))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True, onupdate=text("now()"))

    empresas_usuarios: Mapped[List["EmpresasUsuarios"]] = relationship(
        "EmpresasUsuarios", back_populates="empresa")
