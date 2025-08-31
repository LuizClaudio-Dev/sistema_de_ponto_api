# type:ignore
import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, BigInteger, Date, DateTime,
                        ForeignKeyConstraint, PrimaryKeyConstraint, Text, Time,
                        text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Abonos(Base):
    __tablename__ = 'abonos'
    __table_args__ = (
        PrimaryKeyConstraint('id_abono', name='abonos_pkey'),
        ForeignKeyConstraint(
            ['id_empresa'],
            ['empresas.id_empresa'],
            name='abonos_id_empresa_fkey',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            ['id_usuario_solicitante'],
            ['usuarios.id_usuario'],
            name='abonos_id_usuario_solicitante_fkey',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            ['id_usuario_autorizador'],
            ['usuarios.id_usuario'],
            name='abonos_id_usuario_autorizador_fkey',
            ondelete='NO ACTION',
        )
    )

    id_abono: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_empresa: Mapped[int] = mapped_column(BigInteger, nullable=False)
    id_usuario_solicitante: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    id_usuario_autorizador: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    data_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    periodo: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    anexo: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[int] = mapped_column(DOMAIN('status_solicitacao', SMALLINT(), default='1', constraint_name='status_solicitacao_check',
                                        not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('0'))
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]
                             ] = mapped_column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))

    empresa: Mapped[Optional["Empresas"]] = relationship("Empresas")

    usuario_solicitante: Mapped[Optional["Usuarios"]] = relationship(
        "Usuarios", foreign_keys=[id_usuario_solicitante]
    )
    usuario_autorizador: Mapped[Optional["Usuarios"]] = relationship(
        "Usuarios", foreign_keys=[id_usuario_autorizador]
    )
