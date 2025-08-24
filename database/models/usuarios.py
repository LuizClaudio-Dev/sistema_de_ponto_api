# type: ignore
import datetime
from typing import List, Optional

from sqlalchemy import SMALLINT, TIMESTAMP, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(Text, nullable=False)
    ativo: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1)
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()"))
    data_atualizacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, onupdate=text("now()"))

    empresas_usuarios: Mapped[List["EmpresasUsuarios"]] = relationship(
        "EmpresasUsuarios", back_populates="usuario")
