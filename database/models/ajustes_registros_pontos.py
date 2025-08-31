# type:ignore
import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, BigInteger, DateTime, ForeignKeyConstraint,
                        PrimaryKeyConstraint, Text, Time, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class AjustesRegistrosPontos(Base):
    __tablename__ = 'ajustes_registros_pontos'
    __table_args__ = (
        PrimaryKeyConstraint('id_ajuste_registro_ponto',
                             name='ajustes_registros_ponto_pkey'),
        ForeignKeyConstraint(
            ['id_ajuste'],
            ['ajustes.id_ajuste'],
            name='ajustes_registros_pontos_id_ajuste_fkey',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            ['id_registro_ponto'],
            ['registros_pontos.id_registro_ponto'],
            name='ajustes_registros_pontos_id_registro_ponto_fkey',
            ondelete='NO ACTION',
        ),
    )

    id_ajuste_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, primary_key=True)
    id_ajuste: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    id_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("'-1'::integer"))
    hora_atual: Mapped[Optional[datetime.time]] = mapped_column(Time)
    hora_ajuste: Mapped[Optional[datetime.time]] = mapped_column(Time)
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]
                             ] = mapped_column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))

    ajuste: Mapped[Optional["Ajustes"]] = relationship("Ajustes")
    registro_ponto: Mapped[Optional["RegistrosPontos"]
                           ] = relationship("RegistrosPontos")
