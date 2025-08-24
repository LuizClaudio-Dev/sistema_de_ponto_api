# type: ignore
import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, TIMESTAMP, ForeignKeyConstraint, Integer,
                        Text, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class EmpresasUsuarios(Base):
    __tablename__ = "empresas_usuarios"
    __table_args__ = (
        ForeignKeyConstraint(['id_empresa'], ['empresas.id_empresa'], 'empresas_usuarios_id_empresa_fkey'),
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], 'empresas_usuarios_id_usuario_fkey')
    )

    id_empresa_usuario: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True)
    id_empresa: Mapped[int] = mapped_column(Integer, nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    ativo: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=1)
    motivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_criacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()"))
    data_atualizacao: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, nullable=False, onupdate=text("now()"))

    empresa: Mapped["Empresas"] = relationship(
        "Empresas", back_populates="empresas_usuarios")
    usuario: Mapped["Usuarios"] = relationship(
        "Usuarios", back_populates="empresas_usuarios")
