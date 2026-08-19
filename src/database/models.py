import datetime
import decimal
from typing import List, Optional

from src.database.enums import DiaSemana, TipoPessoa, TipoPeriodo

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (BigInteger, Boolean, CheckConstraint, Date, ForeignKey,
                        Numeric, SmallInteger, String, Text, TIMESTAMP, Time,
                        UniqueConstraint, text)


class CommonBase(Base):
    __abstract__ = True

    ativo: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False)
    excluido: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false"), nullable=False)
    motivo_exclusao: Mapped[Optional[str]] = mapped_column(
        Text, default=None, nullable=True)
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
    __table_args__ = (
        CheckConstraint("pessoa_fisica_juridica IN (1, 2)",
                        name="ck_pessoas_documentos_tipos_pessoa_fisica_juridica"),
    )

    id_pessoa_documento_tipo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    pessoa_fisica_juridica: Mapped[TipoPessoa] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Pessoa física, 2 = Pessoa jurídica")
    descricao: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Descrição do tipo de documento")

    pessoas: Mapped[List["Pessoas"]] = relationship(
        "Pessoas", back_populates="documento_tipo", lazy="raise")


class PessoasDadosAdicionaisTipos(CommonBase):
    __tablename__ = "pessoas_dados_adicionais_tipos"
    __table_args__ = (
        CheckConstraint("pessoa_fisica_juridica IN (1, 2)",
                        name="ck_pessoas_dados_adicionais_tipos_pessoa_fisica_juridica"),
    )

    id_pessoa_dados_adicionais_tipo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    pessoa_fisica_juridica: Mapped[TipoPessoa] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Pessoa física, 2 = Pessoa jurídica")
    descricao: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Descrição do tipo de dado adicional")

    pessoas_dados_adicionais: Mapped[List["PessoasDadosAdicionais"]] = relationship(
        "PessoasDadosAdicionais", back_populates="dados_adicionais_tipos", lazy="raise")

class Cargos(CommonBase):
    __tablename__ = "cargos"

    pessoas_juridicas_fisicas: Mapped[List["PessoasJuridicasFisicas"]] = relationship(
        "PessoasJuridicasFisicas", back_populates="cargos", lazy="raise")

    id_cargo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Descrição do cargo"
    )

class JornadasTrabalho(CommonBase):
    __tablename__ = "jornadas_trabalho"

    pessoas_juridicas_fisicas: Mapped[List["PessoasJuridicasFisicas"]] = relationship(
        "PessoasJuridicasFisicas", back_populates="jornadas_trabalho", lazy="raise")

    id_jornada_trabalho: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Descrição da jornada de trabalho")
    tolerancia_minutos: Mapped[int] = mapped_column(
        SmallInteger, default=0, server_default=text("0"), nullable=False, comment="Tolerância em minutos para batida de ponto")

    periodos: Mapped[List["JornadasTrabalhoPeriodos"]] = relationship(
        "JornadasTrabalhoPeriodos", back_populates="jornada_trabalho", lazy="raise",
        order_by="JornadasTrabalhoPeriodos.dia_semana, JornadasTrabalhoPeriodos.ordem",
        cascade="all, delete-orphan")


class JornadasTrabalhoPeriodos(CommonBase):
    __tablename__ = "jornadas_trabalho_periodos"
    __table_args__ = (
        UniqueConstraint("id_jornada_trabalho", "dia_semana", "ordem",
                         name="uq_jornadas_trabalho_periodos_jornada_dia_ordem"),
        CheckConstraint("hora_inicio < hora_fim",
                        name="ck_jornadas_trabalho_periodos_hora_inicio_fim"),
        CheckConstraint("dia_semana IN (1, 2, 3, 4, 5, 6, 7)",
                        name="ck_jornadas_trabalho_periodos_dia_semana"),
        CheckConstraint("tipo_periodo IN (1, 2)",
                        name="ck_jornadas_trabalho_periodos_tipo_periodo"),
    )

    id_jornada_trabalho_periodo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_jornada_trabalho: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("jornadas_trabalho.id_jornada_trabalho"), nullable=False)
    dia_semana: Mapped[DiaSemana] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Domingo, 2 = Segunda-feira, 3 = Terça-feira, 4 = Quarta-feira, 5 = Quinta-feira, 6 = Sexta-feira, 7 = Sábado"
    )
    tipo_periodo: Mapped[TipoPeriodo] = mapped_column(
        SmallInteger, default=TipoPeriodo.TRABALHO, server_default=text("1"), nullable=False, comment="1 = Trabalho, 2 = Intervalo")
    ordem: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="Ordem dos períodos dentro do dia")
    hora_inicio: Mapped[datetime.time] = mapped_column(
        Time(timezone=False), nullable=False)
    hora_fim: Mapped[datetime.time] = mapped_column(
        Time(timezone=False), nullable=False)


    jornada_trabalho: Mapped["JornadasTrabalho"] = relationship(
        "JornadasTrabalho", back_populates="periodos", lazy="raise")


class Pessoas(CommonBase):
    __tablename__ = "pessoas"
    __table_args__ = (
        CheckConstraint("pessoa_fisica_juridica IN (1, 2)",
                        name="ck_pessoas_pessoa_fisica_juridica"),
    )

    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_documento_tipo: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_documentos_tipos.id_pessoa_documento_tipo"), nullable=False)
    pessoa_fisica_juridica: Mapped[TipoPessoa] = mapped_column(
        SmallInteger, nullable=False)
    documento: Mapped[str] = mapped_column(
        String(140), index=True, nullable=False,
        comment="CPF criptografado (Fernet) para pessoa física ou CNPJ em texto puro para jurídica. Unicidade validada na aplicação.")
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    nome_social: Mapped[Optional[str]] = mapped_column(String(
        100), nullable=True, comment='Nome social caso haja, para pessoas jurídicas, é a razão social')


    documento_tipo: Mapped["PessoasDocumentosTipos"] = relationship(
        "PessoasDocumentosTipos", back_populates="pessoas", lazy="raise")
    enderecos: Mapped[List["PessoasEnderecos"]] = relationship(
        "PessoasEnderecos", back_populates="pessoas", lazy="raise")
    telefones: Mapped[List["PessoasTelefones"]] = relationship(
        "PessoasTelefones", back_populates="pessoas", lazy="raise")
    emails: Mapped[List["PessoasEmails"]] = relationship(
        "PessoasEmails", back_populates="pessoas", lazy="raise")
    dados_adicionais: Mapped[List["PessoasDadosAdicionais"]] = relationship(
        "PessoasDadosAdicionais", back_populates="pessoas", lazy="raise")
    pessoas_juridicas: Mapped[List["PessoasJuridicasFisicas"]] = relationship(
        "PessoasJuridicasFisicas", foreign_keys="PessoasJuridicasFisicas.id_pessoa_juridica", back_populates="pessoa_juridica", lazy="raise")
    pessoas_fisicas: Mapped[List["PessoasJuridicasFisicas"]] = relationship(
        "PessoasJuridicasFisicas", foreign_keys="PessoasJuridicasFisicas.id_pessoa_fisica", back_populates="pessoa_fisica", lazy="raise")
    usuario: Mapped["Usuarios"] = relationship(
        "Usuarios", back_populates="pessoa", lazy="raise")


class PessoasDadosAdicionais(CommonBase):
    __tablename__ = "pessoas_dados_adicionais"

    id_pessoa_dados_adicionais: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    id_pessoa_dados_adicionais_tipo: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_dados_adicionais_tipos.id_pessoa_dados_adicionais_tipo"), nullable=False)
    valor: Mapped[str] = mapped_column(String(200), nullable=False)

    pessoas: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="dados_adicionais", lazy="raise")
    dados_adicionais_tipos: Mapped["PessoasDadosAdicionaisTipos"] = relationship(
        "PessoasDadosAdicionaisTipos", back_populates="pessoas_dados_adicionais", lazy="raise")


class PessoasEnderecos(CommonBase):
    __tablename__ = "pessoas_enderecos"

    id_pessoa_endereco: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    endereco: Mapped[Optional[str]] = mapped_column(Text)
    logradouro: Mapped[Optional[str]] = mapped_column(String(100))
    numero: Mapped[Optional[str]] = mapped_column(String(10))
    complemento: Mapped[Optional[str]] = mapped_column(String(100))
    bairro: Mapped[Optional[str]] = mapped_column(String(100))
    cidade: Mapped[Optional[str]] = mapped_column(String(100))
    uf: Mapped[Optional[str]] = mapped_column(String(2))
    cep: Mapped[Optional[str]] = mapped_column(String(9))
    principal: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False)

    pessoas: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="enderecos", lazy="raise")


class PessoasTelefones(CommonBase):
    __tablename__ = "pessoas_telefones"

    id_pessoa_telefone: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    ddd: Mapped[str] = mapped_column(String(2), nullable=False)
    telefone: Mapped[str] = mapped_column(String(11), nullable=False)
    principal: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False)

    pessoas: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="telefones", lazy="raise")


class PessoasEmails(CommonBase):
    __tablename__ = "pessoas_emails"

    id_pessoa_email: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    principal: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False)

    pessoas: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="emails", lazy="raise")


class PessoasRelacoesTipos(CommonBase):
    __tablename__ = "pessoas_relacoes_tipos"

    id_pessoa_relacao_tipo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Descrição do tipo de relação")

    pessoas_juridicas_fisicas: Mapped[List["PessoasJuridicasFisicas"]] = relationship(
        "PessoasJuridicasFisicas", back_populates="pessoas_relacoes_tipos", lazy="raise")


class PessoasJuridicasFisicas(CommonBase):
    __tablename__ = "pessoas_juridicas_fisicas"
    __table_args__ = (
        UniqueConstraint("id_pessoa_juridica", "matricula",
                         name="uq_pessoas_juridicas_fisicas_juridica_matricula"),
        CheckConstraint("id_pessoa_juridica <> id_pessoa_fisica",
                        name="ck_pessoas_juridicas_fisicas_nao_auto_relacao"),
        CheckConstraint("data_desligamento IS NULL OR data_desligamento >= data_admissao",
                        name="ck_pessoas_juridicas_fisicas_desligamento_admissao"),
        CheckConstraint("salario IS NULL OR salario >= 0",
                        name="ck_pessoas_juridicas_fisicas_salario"),
    )

    id_pessoa_juridica_fisica: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa_juridica: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    id_pessoa_fisica: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    id_pessoa_relacao_tipo: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_relacoes_tipos.id_pessoa_relacao_tipo"), nullable=False)
    id_cargo: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("cargos.id_cargo"), nullable=False)
    id_jornada_trabalho: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("jornadas_trabalho.id_jornada_trabalho"), nullable=False
    )
    matricula: Mapped[Optional[str]] = mapped_column(String(100))
    data_admissao: Mapped[Optional[datetime.date]] = mapped_column(
        Date, nullable=True)
    data_desligamento: Mapped[Optional[datetime.date]] = mapped_column(Date)
    salario: Mapped[Optional[decimal.Decimal]] = mapped_column(
        Numeric(18, 2), nullable=True)

    pessoa_juridica: Mapped["Pessoas"] = relationship(
        "Pessoas", foreign_keys=[id_pessoa_juridica], back_populates="pessoas_juridicas", lazy="raise")
    pessoa_fisica: Mapped["Pessoas"] = relationship(
        "Pessoas", foreign_keys=[id_pessoa_fisica], back_populates="pessoas_fisicas", lazy="raise")
    pessoas_relacoes_tipos: Mapped["PessoasRelacoesTipos"] = relationship(
        "PessoasRelacoesTipos", back_populates="pessoas_juridicas_fisicas", lazy="raise")
    cargos: Mapped["Cargos"] = relationship(
        "Cargos", back_populates="pessoas_juridicas_fisicas", lazy="raise")
    jornadas_trabalho: Mapped["JornadasTrabalho"] = relationship(
        "JornadasTrabalho", back_populates="pessoas_juridicas_fisicas", lazy="raise")


class Usuarios(CommonBase):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False, unique=True, index=True)
    login: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(Text, nullable=False)
    is_master: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false"), nullable=False)

    pessoa: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="usuario", lazy="raise")
