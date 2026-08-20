"""seed_perfis_permissoes

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-20 18:24:32.045502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Perfis padrão
PERFIS = [
    (1, "Administrador"),
    (2, "Gerente"),
    (3, "Funcionário"),
]

# Permissões por módulo (chave, modulo, descricao)
# Módulos: 1=Usuarios 2=Perfis 3=Permissoes 4=Vinculos 5=Cargos 6=Jornadas
#          7=RegistrosPontos 8=Abonos 9=Ajustes 10=Feriados 11=Configuracoes 12=Pessoas
PERMISSOES = [
    # Usuarios
    ("usuarios.visualizar", 1, "Visualizar usuários"),
    ("usuarios.criar", 1, "Criar usuários"),
    ("usuarios.editar", 1, "Editar usuários"),
    ("usuarios.excluir", 1, "Excluir usuários"),
    # Perfis
    ("perfis.visualizar", 2, "Visualizar perfis"),
    ("perfis.criar", 2, "Criar perfis"),
    ("perfis.editar", 2, "Editar perfis"),
    ("perfis.excluir", 2, "Excluir perfis"),
    # Permissoes
    ("permissoes.visualizar", 3, "Visualizar permissões"),
    ("permissoes.criar", 3, "Criar permissões"),
    ("permissoes.editar", 3, "Editar permissões"),
    ("permissoes.excluir", 3, "Excluir permissões"),
    # Vinculos
    ("vinculos.visualizar", 4, "Visualizar vínculos"),
    ("vinculos.criar", 4, "Criar vínculos"),
    ("vinculos.editar", 4, "Editar vínculos"),
    ("vinculos.excluir", 4, "Excluir vínculos"),
    # Cargos
    ("cargos.visualizar", 5, "Visualizar cargos"),
    ("cargos.criar", 5, "Criar cargos"),
    ("cargos.editar", 5, "Editar cargos"),
    ("cargos.excluir", 5, "Excluir cargos"),
    # Jornadas
    ("jornadas.visualizar", 6, "Visualizar jornadas"),
    ("jornadas.criar", 6, "Criar jornadas"),
    ("jornadas.editar", 6, "Editar jornadas"),
    ("jornadas.excluir", 6, "Excluir jornadas"),
    # Registros de Ponto
    ("registros_pontos.registrar", 7, "Registrar ponto"),
    ("registros_pontos.visualizar", 7, "Visualizar registros de ponto"),
    ("registros_pontos.editar", 7, "Editar registros de ponto"),
    ("registros_pontos.excluir", 7, "Excluir registros de ponto"),
    # Abonos
    ("abonos.solicitar", 8, "Solicitar abonos"),
    ("abonos.visualizar", 8, "Visualizar abonos"),
    ("abonos.aprovar", 8, "Aprovar abonos"),
    ("abonos.editar", 8, "Editar abonos"),
    ("abonos.excluir", 8, "Excluir abonos"),
    # Ajustes
    ("ajustes.solicitar", 9, "Solicitar ajustes"),
    ("ajustes.visualizar", 9, "Visualizar ajustes"),
    ("ajustes.aprovar", 9, "Aprovar ajustes"),
    ("ajustes.editar", 9, "Editar ajustes"),
    ("ajustes.excluir", 9, "Excluir ajustes"),
    # Feriados
    ("feriados.visualizar", 10, "Visualizar feriados"),
    ("feriados.criar", 10, "Criar feriados"),
    ("feriados.editar", 10, "Editar feriados"),
    ("feriados.excluir", 10, "Excluir feriados"),
    # Configuracoes
    ("configuracoes.visualizar", 11, "Visualizar configurações"),
    ("configuracoes.editar", 11, "Editar configurações"),
    # Pessoas
    ("pessoas.visualizar", 12, "Visualizar pessoas"),
    ("pessoas.criar", 12, "Criar pessoas"),
    ("pessoas.editar", 12, "Editar pessoas"),
    ("pessoas.excluir", 12, "Excluir pessoas"),
]

# Chaves de permissão por perfil
PERFIL_PERMISSOES = {
    "Administrador": [p[0] for p in PERMISSOES],
    "Gerente": [
        # Visualiza tudo
        "usuarios.visualizar", "perfis.visualizar", "permissoes.visualizar",
        "vinculos.visualizar", "cargos.visualizar", "jornadas.visualizar",
        "feriados.visualizar", "configuracoes.visualizar", "pessoas.visualizar",
        # Registros
        "registros_pontos.visualizar", "registros_pontos.editar", "registros_pontos.excluir",
        # Abonos
        "abonos.visualizar", "abonos.aprovar",
        # Ajustes
        "ajustes.visualizar", "ajustes.aprovar",
    ],
    "Funcionário": [
        "registros_pontos.registrar", "registros_pontos.visualizar",
        "abonos.solicitar", "abonos.visualizar",
        "ajustes.solicitar", "ajustes.visualizar",
    ],
}


def _insert(table: str, columns: str, rows: list[tuple]) -> None:
    """Executa INSERTs com bind params nomeados, incluindo data_criacao com CURRENT_TIMESTAMP (portável)."""
    bind = op.get_bind()
    col_names = [c.strip() for c in columns.split(",")]
    cols_sql = ", ".join(col_names + ["data_criacao"])
    placeholders = ", ".join([f":{c}" for c in col_names] + ["CURRENT_TIMESTAMP"])
    sql = f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})"
    for row in rows:
        bind.execute(sa.text(sql), dict(zip(col_names, row)))


def upgrade() -> None:
    """Upgrade schema."""
    # Perfis
    _insert("perfis", "id_perfil, descricao", PERFIS)

    # Permissões (id_permissao explícito para funcionar no SQLite, onde BIGINT PK não autoincrementa)
    _insert(
        "permissoes",
        "id_permissao, chave, modulo, descricao",
        [(idx + 1, chave, modulo, descricao) for idx, (chave, modulo, descricao) in enumerate(PERMISSOES)],
    )

    # Perfis x Permissões
    permissao_ids = {chave: idx + 1 for idx, (chave, _, _) in enumerate(PERMISSOES)}
    perfil_ids = {descricao: pid for pid, descricao in PERFIS}
    rows = []
    seq = 1
    for perfil_desc, chaves in PERFIL_PERMISSOES.items():
        for chave in chaves:
            rows.append((seq, perfil_ids[perfil_desc], permissao_ids[chave]))
            seq += 1
    _insert("perfis_permissoes", "id_perfil_permissao, id_perfil, id_permissao", rows)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM perfis_permissoes WHERE id_perfil IN (1, 2, 3)")
    op.execute("DELETE FROM perfis WHERE id_perfil IN (1, 2, 3)")
    op.execute("DELETE FROM permissoes WHERE modulo BETWEEN 1 AND 12")
