
import datetime
from typing import Optional

from sqlalchemy import (BigInteger, DateTime, ForeignKeyConstraint,
                        PrimaryKeyConstraint, Text, text)
from sqlalchemy.dialects.postgresql import DOMAIN, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class PerfisPermissoes(Base):
    __tablename__ = 'perfis_permissoes'
    __table_args__ = (
        PrimaryKeyConstraint('id_perfil_permissao',
                             name='perfis_permissoes_pkey'),
        ForeignKeyConstraint(
            ['id_perfil'],
            ['perfis.id_perfil'],
            name='perfis_permissoes_id_perfil_fkey',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            ['id_permissao'],
            ['permissoes.id_permissao'],
            name='perfis_permissoes_id_permissao_fkey',
            ondelete='NO ACTION',
        ),
    )

    id_perfil_permissao: Mapped[int] = mapped_column(
        BigInteger, primary_key=True)
    id_perfil: Mapped[int] = mapped_column(BigInteger, nullable=False)
    id_permissao: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ativo: Mapped[int] = mapped_column(
        DOMAIN('status_registro', SMALLINT(), default='1', constraint_name='status_registro_check',
               not_null=True, check=text('VALUE = ANY (ARRAY[0, 1, 2])')), nullable=False, server_default=text('1')
    )
    motivo: Mapped[Optional[str]] = mapped_column(Text)
    data_criacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]
                             ] = mapped_column(DateTime, onupdate=text('CURRENT_TIMESTAMP'))
