import datetime
from typing import Optional

from sqlalchemy import (SMALLINT, BigInteger, DateTime, PrimaryKeyConstraint,
                        String, Text, text)
from sqlalchemy.dialects.postgresql import DOMAIN
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Permissoes(Base):
    __tablename__ = 'permissoes'

    __table_args__ = (
        PrimaryKeyConstraint('id_permissao', name='permissoes_pkey'),
    )

    id_permissao: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100), nullable=False)
    ativo: Mapped[int] = mapped_column(DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
                                       not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1'))
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]
                             ] = mapped_column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))
