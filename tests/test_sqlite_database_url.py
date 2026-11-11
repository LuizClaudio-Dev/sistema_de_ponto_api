import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.settings import Settings


def test_sqlite_test_database_connects(tmp_path):
    database_file = tmp_path / "sistema-ponto-test.db"
    settings = Settings(
        _env_file=None,
        environment="test",
        api_name="sistema-ponto-test",
        jwt_secret_key="test-only-secret",
        jwt_algorithm="HS256",
        fernet_secret_key="test-only-key",
        database_driver="sqlite+aiosqlite",
        database_user=None,
        database_password=None,
        database_host=None,
        database_port=None,
        database_name=str(database_file),
        database_sslmode="disable",
    )

    async def check_connection():
        engine = create_async_engine(settings.database_url)
        try:
            async with engine.connect() as connection:
                result = await connection.execute(text("SELECT 1"))
                assert result.scalar_one() == 1
        finally:
            await engine.dispose()

    asyncio.run(check_connection())
    assert database_file.is_file()
