import datetime
from typing import Optional

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Boolean, SmallInteger, String, Text, TIMESTAMP, text


class CommonBase(Base):
    __abstract__ = True

    ativo: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=True, nullable=False)
    excluido: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=False, nullable=False)
    motivo_exclusao: Mapped[str] = mapped_column(
        Text, default=None, server_default=None)
    data_criacao: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=False),
                                                            nullable=False,
                                                            default=datetime.datetime.now,
                                                            server_default=text('now()'))
    data_atualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP(timezone=False),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        server_onupdate=text('now()'),
    )


class PessoasDocumentosTipos(CommonBase):
    __tablename__ = "pessoas_documentos_tipos"
    __options__ = {"comment": "Tabela para representar possíveis tipos de documentos em comum para pessoas"}

    id_pessoa_documento_tipo: Mapped[int] = mapped_column(BigInteger,primary_key=True, autoincrement=True)
    pessoa_tipo: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    descricao: Mapped[str] = mapped_column(String(100), nullable=False)

class Pessoas(CommonBase):
    __tablename__ = "pessoas"

    id_pessoa: Mapped[int] = mapped_column(BigInteger,primary_key=True, autoincrement=True)
    tipo_documento: Mapped[str] = mapped_column(String(2), nullable=False)
    documento: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    nome_social: Mapped[str] = mapped_column(String(100), nullable=False)
