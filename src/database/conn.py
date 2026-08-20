from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.settings import get_settings

settings = get_settings()
# SQLALCHEMY_DATABASE_URL = "driver://user:password@server/dbname"

engine_kwargs = {}

if not settings.is_sqlite:
    engine_kwargs.update(
        {
            # Mantém um número fixo de conexões abertas para evitar overhead de criação/destruição frequente
            "pool_size": settings.database_pool_size,
            # Permite um número limitado de conexões extras para lidar com picos de tráfego, mas sem criar muitas conexões desnecessárias
            "max_overflow": settings.database_pool_max_overflow,
            # Define um tempo limite razoável para obter uma conexão do pool, evitando bloqueios prolongados
            "pool_timeout": settings.database_pool_timeout,
            # Habilita o pre-ping para garantir que as conexões sejam válidas antes de usá-las, evitando erros de conexão
            "pool_pre_ping": settings.database_pool_pre_ping,
            # Recicla conexões após um certo tempo para evitar problemas de conexões antigas ou inativas, especialmente em ambientes de produção
            "pool_recycle": settings.database_pool_recycle,
            # Usa LIFO para reutilizar conexões mais recentemente usadas, o que pode melhorar a performance em cenários de alta concorrência
            "pool_use_lifo": settings.database_pool_use_lifo,
            # Adiciona o nome da aplicação para facilitar o monitoramento e identificação das conexões no banco de dados
            "connect_args": {"application_name": settings.api_name},
        }
    )

engine = create_async_engine(
    settings.database_url,
    **engine_kwargs
)

# Cria a fábrica de sessões do SQLAlchemy, que será usada para criar sessões de banco de dados em toda a aplicação
session_factory = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)

# Gerador de sessão para ser usado como dependência no FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# Gerador de sessão com Context manager para usar com "with",
# e garantir fechamento da sessão em qualquer função que precise de acesso ao banco de dados
@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
