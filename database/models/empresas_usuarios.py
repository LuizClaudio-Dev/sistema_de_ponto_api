# type: ignore
import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, TIMESTAMP, ForeignKeyConstraint, Integer,
                        PrimaryKeyConstraint, Text, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class EmpresasUsuarios(Base):
    __tablename__ = "empresas_usuarios"
    __table_args__ = (
        PrimaryKeyConstraint("id_empresa_usuario",
                             name="empresas_usuarios_pkey"),
        ForeignKeyConstraint(
            ['id_empresa'], ['empresas.id_empresa'], 'empresas_usuarios_id_empresa_fkey'),
        ForeignKeyConstraint(
            ['id_usuario'], ['usuarios.id_usuario'], 'empresas_usuarios_id_usuario_fkey'),
        {"sqlite_autoincrement": True},
    )

    id_empresa_usuario: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    id_empresa: Mapped[int] = mapped_column(Integer, nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    ativo: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1)
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, nullable=True, onupdate=text("CURRENT_TIMESTAMP"))

    empresa: Mapped["Empresas"] = relationship(
        "Empresas", back_populates="empresas_usuarios")
    usuario: Mapped["Usuarios"] = relationship(
        "Usuarios", back_populates="empresas_usuarios")
