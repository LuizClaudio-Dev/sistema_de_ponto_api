# type: ignore
import datetime
from typing import List, Optional

from sqlalchemy import (SMALLINT, TIMESTAMP, Integer, PrimaryKeyConstraint,
                        String, Text, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Usuarios(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        PrimaryKeyConstraint("id_usuario", name="usuarios_pkey"),
    )

    id_usuario: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    pis: Mapped[Optional[str]] = mapped_column(
        String(11), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(Text, nullable=False)
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True, onupdate=text("CURRENT_TIMESTAMP"))

    empresas_usuarios: Mapped[List["EmpresasUsuarios"]] = relationship(
        "EmpresasUsuarios", back_populates="usuario")
