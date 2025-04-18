from abc import ABC, abstractmethod

import asyncpg


class DBStrategy(ABC):
    """Interface for database strategies."""

    @abstractmethod
    async def generate_db_url(self, tenant_id: str, settings) -> str:
        pass

    @abstractmethod
    async def create_db_if_needed(self, tenant_id: str, settings) -> None:
        pass


class SQLiteStrategy(DBStrategy):
    """SQLite strategy for working with SQLite."""

    async def generate_db_url(self, tenant_id: str, settings) -> str:
        return f"sqlite://tenant_{tenant_id}.db"

    async def create_db_if_needed(self, tenant_id: str, settings) -> None:
        pass


class PostgresStrategy(DBStrategy):
    """Strategy for working with PostgreSQL."""

    async def generate_db_url(self, tenant_id: str, settings) -> str:

        has_port = settings.TENANT_DB_PORT
        port = f":{has_port}" if has_port else ""

        pwd = settings.TENANT_DB_PASSWORD
        username = settings.TENANT_DB_USER
        user_pwd = f"{username}:{pwd}"
        auth = f"{user_pwd}@" if username else ""

        db_name = f"tenant_{tenant_id}"

        return f"postgres://{auth}{settings.TENANT_DB_HOST}{port}/{db_name}"

    async def create_db_if_needed(self, tenant_id: str, settings) -> None:
        db_name = f"tenant_{tenant_id}"

        try:
            conn = await asyncpg.connect(
                host=settings.TENANT_DB_HOST,
                port=int(settings.TENANT_DB_PORT) if settings.TENANT_DB_PORT else 5432,
                user=settings.TENANT_DB_USER,
                password=settings.TENANT_DB_PASSWORD,
                database="postgres",
            )

            exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)",
                db_name,
            )

            if not exists:
                await conn.execute(f'CREATE DATABASE "{db_name}"')
                print(f"Database {db_name} created")

            await conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")


def get_db_strategy(driver: str):
    strategies = {
        "sqlite": SQLiteStrategy(),
        "postgres": PostgresStrategy(),
    }
    return strategies.get(driver, SQLiteStrategy())
