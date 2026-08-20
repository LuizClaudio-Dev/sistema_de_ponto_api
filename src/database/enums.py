
from enum import IntEnum

class CommonIntEnum(IntEnum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values(cls):
        return [key.value for key in cls]

    @classmethod
    def names(cls):
        return [key.name for key in cls]

class TipoPessoa(CommonIntEnum):
    FISICA = 1
    JURIDICA = 2


class DiaSemana(CommonIntEnum):
    DOMINGO = 1
    SEGUNDA = 2
    TERCA = 3
    QUARTA = 4
    QUINTA = 5
    SEXTA = 6
    SABADO = 7


class TipoPeriodo(CommonIntEnum):
    TRABALHO = 1
    INTERVALO = 2


class TipoBatida(CommonIntEnum):
    ENTRADA = 1
    SAIDA = 2


class StatusSolicitacao(CommonIntEnum):
    PENDENTE = 1
    APROVADO = 2
    REJEITADO = 3


class TipoFeriado(CommonIntEnum):
    NACIONAL = 1
    ESTADUAL = 2
    MUNICIPAL = 3
    EMPRESA = 4

class ModulosSistema(CommonIntEnum):
    USUARIOS = 1
    PERFIS = 2
    PERMISSOES = 3
    VINCULOS = 4 # pessoas_juridicas_fisicas
    CARGOS = 5
    JORNADAS = 6 # jornadas_trabalho
    REGISTROS_PONTOS = 7 # registros_pontos
    ABONOS = 8
    AJUSTES = 9
    FERIADOS = 10
    CONFIGURACOES = 11
    PESSOAS = 12 # Cadastro de pessoas físicas / jurídicas