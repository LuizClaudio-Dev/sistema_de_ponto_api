from pydantic import BaseModel, Field


class Paginacao(BaseModel):
    total: int = Field(0)  # total de registros no banco
    pagina: int = Field(1)  # página atual
    registros_por_pagina: int = Field(10)  # quantos registros por página
    total_paginas: int = Field(10)  # total de páginas
