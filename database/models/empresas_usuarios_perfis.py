# type:ignore
import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, BigInteger, DateTime, ForeignKeyConstraint,
                        PrimaryKeyConstraint, Text, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class EmpresasUsuariosPerfis(Base):
    __tablename__ = 'empresas_usuarios_perfis'
    __table_args__ = (
        PrimaryKeyConstraint('id_empresa_usuario_perfil',
                             name='empresas_usuarios_perfis_pkey'),
        ForeignKeyConstraint(
            ['id_empresa'],
            ['empresas.id_empresa'],
            name='empresas_usuarios_perfis_id_empresa_fkey',
            ondelete='NO ACTION'),
        ForeignKeyConstraint(
            ['id_usuario'],
            ['usuarios.id_usuario'],
            name='empresas_usuarios_perfis_id_usuario_fkey',
            ondelete='NO ACTION'),
        ForeignKeyConstraint(
            ['id_perfil'],
            ['perfis.id_perfil'],
            name='empresas_usuarios_perfis_id_perfil_fkey'),
    )

    id_empresa_usuario_perfil: Mapped[int] = mapped_column(
        BigInteger, primary_key=True)
    id_empresa: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    id_usuario: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    id_perfil: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, onupdate=text("CURRENT_TIMESTAMP"))
