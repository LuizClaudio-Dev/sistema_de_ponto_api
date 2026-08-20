import datetime
import decimal
from typing import List, Optional

from src.database.enums import (DiaSemana, StatusSolicitacao, TipoBatida,
                                TipoFeriado, TipoPessoa, TipoPeriodo)

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
    configuracoes: Mapped[List["PessoasConfiguracoes"]] = relationship(
        "PessoasConfiguracoes", back_populates="pessoa", lazy="raise")


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
    registros_pontos: Mapped[List["RegistrosPontos"]] = relationship(
        "RegistrosPontos", back_populates="vinculo", lazy="raise")
    abonos: Mapped[List["Abonos"]] = relationship(
        "Abonos", back_populates="vinculo", lazy="raise")
    ajustes: Mapped[List["Ajustes"]] = relationship(
        "Ajustes", back_populates="vinculo", lazy="raise")


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
    abonos_autorizados: Mapped[List["Abonos"]] = relationship(
        "Abonos", foreign_keys="Abonos.id_usuario_autorizador", back_populates="usuario_autorizador", lazy="raise")
    ajustes_autorizados: Mapped[List["Ajustes"]] = relationship(
        "Ajustes", foreign_keys="Ajustes.id_usuario_autorizador", back_populates="usuario_autorizador", lazy="raise")
    anexos_enviados: Mapped[List["AbonosAnexos"]] = relationship(
        "AbonosAnexos", foreign_keys="AbonosAnexos.id_usuario_upload", back_populates="usuario_upload", lazy="raise")


class RegistrosPontos(CommonBase):
    __tablename__ = "registros_pontos"
    __table_args__ = (
        CheckConstraint("tipo IN (1, 2)",
                        name="ck_registros_pontos_tipo"),
        CheckConstraint("latitude IS NULL OR latitude BETWEEN -90 AND 90",
                        name="ck_registros_pontos_latitude"),
        CheckConstraint("longitude IS NULL OR longitude BETWEEN -180 AND 180",
                        name="ck_registros_pontos_longitude"),
    )

    id_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa_juridica_fisica: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_juridicas_fisicas.id_pessoa_juridica_fisica"), nullable=False)
    tipo: Mapped[TipoBatida] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Entrada, 2 = Saída")
    data_hora_ponto: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False, comment="Data e hora exatas da batida")
    latitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(11, 8))
    foto: Mapped[Optional[str]] = mapped_column(
        Text, comment="Caminho/URL da foto do funcionário na batida. Obrigatoriedade definida por configuração da empresa.")


    vinculo: Mapped["PessoasJuridicasFisicas"] = relationship(
        "PessoasJuridicasFisicas", back_populates="registros_pontos", lazy="raise")
    ajustes_registros_pontos: Mapped[List["AjustesRegistrosPontos"]] = relationship(
        "AjustesRegistrosPontos", back_populates="registro_ponto", lazy="raise")


class Abonos(CommonBase):
    __tablename__ = "abonos"
    __table_args__ = (
        CheckConstraint("minutos_abono > 0",
                        name="ck_abonos_minutos_abono"),
        CheckConstraint("status IN (1, 2, 3)",
                        name="ck_abonos_status"),
    )

    id_abono: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa_juridica_fisica: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_juridicas_fisicas.id_pessoa_juridica_fisica"), nullable=False)
    id_usuario_autorizador: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("usuarios.id_usuario"))
    data: Mapped[datetime.date] = mapped_column(
        Date, nullable=False, comment="Dia do abono")
    minutos_abono: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, comment="Minutos abonados no dia. Não pode exceder a duração da jornada do dia (validado na aplicação).")
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[StatusSolicitacao] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Pendente, 2 = Aprovado, 3 = Rejeitado")


    vinculo: Mapped["PessoasJuridicasFisicas"] = relationship(
        "PessoasJuridicasFisicas", back_populates="abonos", lazy="raise")
    usuario_autorizador: Mapped[Optional["Usuarios"]] = relationship(
        "Usuarios", foreign_keys=[id_usuario_autorizador], back_populates="abonos_autorizados", lazy="raise")
    anexos: Mapped[List["AbonosAnexos"]] = relationship(
        "AbonosAnexos", back_populates="abono", lazy="raise",
        cascade="all, delete-orphan")


class AbonosAnexos(CommonBase):
    __tablename__ = "abonos_anexos"

    id_abono_anexo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_abono: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("abonos.id_abono"), nullable=False)
    id_usuario_upload: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("usuarios.id_usuario"), nullable=False)
    nome_original: Mapped[str] = mapped_column(String(255), nullable=False)
    caminho: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Caminho/URL do arquivo no storage")
    tipo_mime: Mapped[Optional[str]] = mapped_column(String(100))
    tamanho_bytes: Mapped[Optional[int]] = mapped_column(BigInteger)
    hash: Mapped[Optional[str]] = mapped_column(String(64))

    abono: Mapped["Abonos"] = relationship(
        "Abonos", back_populates="anexos", lazy="raise")
    usuario_upload: Mapped["Usuarios"] = relationship(
        "Usuarios", foreign_keys=[id_usuario_upload], back_populates="anexos_enviados", lazy="raise")


class Ajustes(CommonBase):
    __tablename__ = "ajustes"
    __table_args__ = (
        CheckConstraint("status IN (1, 2, 3)",
                        name="ck_ajustes_status"),
    )

    id_ajuste: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa_juridica_fisica: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_juridicas_fisicas.id_pessoa_juridica_fisica"), nullable=False)
    id_usuario_autorizador: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("usuarios.id_usuario"))
    data: Mapped[datetime.date] = mapped_column(
        Date, nullable=False, comment="Dia dos registros de ponto afetados pelo ajuste")
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[StatusSolicitacao] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Pendente, 2 = Aprovado, 3 = Rejeitado")


    vinculo: Mapped["PessoasJuridicasFisicas"] = relationship(
        "PessoasJuridicasFisicas", back_populates="ajustes", lazy="raise")
    usuario_autorizador: Mapped[Optional["Usuarios"]] = relationship(
        "Usuarios", foreign_keys=[id_usuario_autorizador], back_populates="ajustes_autorizados", lazy="raise")
    ajustes_registros_pontos: Mapped[List["AjustesRegistrosPontos"]] = relationship(
        "AjustesRegistrosPontos", back_populates="ajuste", lazy="raise",
        cascade="all, delete-orphan")


class AjustesRegistrosPontos(CommonBase):
    __tablename__ = "ajustes_registros_pontos"
    __table_args__ = (
        UniqueConstraint("id_ajuste", "id_registro_ponto",
                         name="uq_ajustes_registros_pontos_ajuste_registro"),
    )

    id_ajuste_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_ajuste: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("ajustes.id_ajuste"), nullable=False)
    id_registro_ponto: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("registros_pontos.id_registro_ponto"), nullable=False)
    hora_atual: Mapped[Optional[datetime.time]] = mapped_column(Time)
    hora_ajuste: Mapped[Optional[datetime.time]] = mapped_column(Time)


    ajuste: Mapped["Ajustes"] = relationship(
        "Ajustes", back_populates="ajustes_registros_pontos", lazy="raise")
    registro_ponto: Mapped["RegistrosPontos"] = relationship(
        "RegistrosPontos", back_populates="ajustes_registros_pontos", lazy="raise")


class Feriados(CommonBase):
    __tablename__ = "feriados"
    __table_args__ = (
        UniqueConstraint("data_feriado", name="uq_feriados_data_feriado"),
        CheckConstraint("tipo IN (1, 2, 3, 4)",
                        name="ck_feriados_tipo"),
    )

    id_feriado: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    data_feriado: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    tipo: Mapped[TipoFeriado] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Nacional, 2 = Estadual, 3 = Municipal, 4 = Empresa")
    descricao: Mapped[Optional[str]] = mapped_column(Text)



class PessoasConfiguracoesTipos(CommonBase):
    __tablename__ = "pessoas_configuracoes_tipos"
    __table_args__ = (
        UniqueConstraint("chave", name="uq_pessoas_configuracoes_tipos_chave"),
        CheckConstraint("pessoa_fisica_juridica IN (1, 2)",
                        name="ck_pessoas_configuracoes_tipos_pessoa_fisica_juridica"),
    )

    id_pessoa_configuracao_tipo: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    pessoa_fisica_juridica: Mapped[TipoPessoa] = mapped_column(
        SmallInteger, nullable=False, comment="1 = Pessoa física, 2 = Pessoa jurídica")
    chave: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Chave identificadora da configuração")
    descricao: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="Descrição da configuração")
    tipo_valor: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Tipo do valor: boolean, integer, decimal, text, json")


    configuracoes: Mapped[List["PessoasConfiguracoes"]] = relationship(
        "PessoasConfiguracoes", back_populates="configuracao_tipo", lazy="raise")


class PessoasConfiguracoes(CommonBase):
    __tablename__ = "pessoas_configuracoes"
    __table_args__ = (
        UniqueConstraint("id_pessoa", "id_pessoa_configuracao_tipo",
                         name="uq_pessoas_configuracoes_pessoa_tipo"),
    )

    id_pessoa_configuracao: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas.id_pessoa"), nullable=False)
    id_pessoa_configuracao_tipo: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pessoas_configuracoes_tipos.id_pessoa_configuracao_tipo"), nullable=False)
    valor: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Valor da configuração, interpretado pela aplicação conforme tipo_valor")


    pessoa: Mapped["Pessoas"] = relationship(
        "Pessoas", back_populates="configuracoes", lazy="raise")
    configuracao_tipo: Mapped["PessoasConfiguracoesTipos"] = relationship(
        "PessoasConfiguracoesTipos", back_populates="configuracoes", lazy="raise")
