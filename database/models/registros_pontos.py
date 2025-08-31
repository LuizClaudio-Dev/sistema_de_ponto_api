# type:ignore
import datetime
import decimal
from typing import Optional

from sqlalchemy import (SMALLINT, BigInteger, DateTime, ForeignKeyConstraint,
                        Numeric, PrimaryKeyConstraint, Text, Time, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class RegistrosPontos(Base):
    __tablename__ = 'registros_pontos'
    __table_args__ = (
        PrimaryKeyConstraint('id_registro_ponto',
                             name='registros_pontos_pkey'),
        ForeignKeyConstraint(
            ['id_empresa'],
            ['empresas.id_empresa'],
            name='registros_pontos_id_empresa_fkey',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            ['id_usuario'],
            ['usuarios.id_usuario'],
            name='registros_pontos_id_usuario_fkey',
            ondelete='NO ACTION',
        ),
    )

    id_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, primary_key=True)
    id_empresa: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    id_usuario: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    tipo: Mapped[int] = mapped_column(DOMAIN('tipo_registro_ponto', SMALLINT(), default='0', constraint_name='tipo_registro_ponto_check',
                                      not_null=True, check=text('VALUE = ANY (ARRAY[0, 1])')), nullable=False, server_default=text('0'))
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Optional[decimal.Decimal]
                      ] = mapped_column(Numeric(11, 8))
    foto: Mapped[Optional[str]] = mapped_column(Text)
    saldo_horas: Mapped[Optional[datetime.time]] = mapped_column(Time)
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]
                             ] = mapped_column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))

    empresa: Mapped[Optional["Empresas"]] = relationship("Empresas")
    usuario: Mapped[Optional["Usuarios"]] = relationship("Usuarios")
