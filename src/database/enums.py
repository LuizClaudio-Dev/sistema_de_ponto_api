
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
