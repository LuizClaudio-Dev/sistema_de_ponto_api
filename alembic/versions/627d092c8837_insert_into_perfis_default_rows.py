"""insert_into_perfis_default_rows

Revision ID: 627d092c8837
Revises: 79fa9217f75f
Create Date: 2025-08-31 13:54:48.680829

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '627d092c8837'
down_revision: Union[str, Sequence[str], None] = '79fa9217f75f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criando os perfis sem ID para que o próprio "generator" do PostgreSQL seja utilizado
    op.execute("INSERT INTO perfis (descricao) VALUES ('Administrador')")
    op.execute("INSERT INTO perfis (descricao) VALUES ('Gerência')")
    op.execute("INSERT INTO perfis (descricao) VALUES ('Supervisor')")
    op.execute("INSERT INTO perfis (descricao) VALUES ('Funcionario')")


def downgrade() -> None:
    op.execute("DELETE FROM perfis")
    op.execute("ALTER SEQUENCE perfis_id_perfil_seq RESTART WITH 1")
