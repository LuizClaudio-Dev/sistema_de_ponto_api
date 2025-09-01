"""insert_default_permissions

Revision ID: e389a379712f
Revises: cbfc7b6752fe
Create Date: 2025-08-31 21:07:16.984042

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e389a379712f'
down_revision: Union[str, Sequence[str], None] = 'cbfc7b6752fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Empresas')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Empresas')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Empresas')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Empresas')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Empresas')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Usuários')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Usuários')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Usuários')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Usuários')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Usuários')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Perfis')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Perfis')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Perfis')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Perfis')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Perfis')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Gerenciar Permissões')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Visualizar Permissões')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Permissões')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Permissões')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Permissões')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Gerenciar Registros de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Visualizar Registros de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Criar Registros de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Editar Registros de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Excluir Registros de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Gerenciar Ajustes de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Visualizar Ajustes de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Criar Ajustes de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Editar Ajustes de Ponto')")
    op.execute(
        "INSERT INTO permissoes (descricao) VALUES ('Excluir Ajustes de Ponto')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Abonos')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Abonos')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Abonos')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Abonos')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Abonos')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Feriados')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Feriados')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Feriados')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Feriados')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Feriados')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Gerenciar Ajustes')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Visualizar Ajustes')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Criar Ajustes')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Editar Ajustes')")
    op.execute("INSERT INTO permissoes (descricao) VALUES ('Excluir Ajustes')")


def downgrade() -> None:
    op.execute("DELETE FROM permissoes")
    op.execute("ALTER SEQUENCE permissoes_id_permissao_seq RESTART WITH 1")
