from __future__ import annotations

from typing import Dict, List, Optional

from tortoise import Tortoise

from settings import get_settings

from .db_strategy import get_db_strategy


class DBManager:
    """Singleton managing core and tenant connections."""

    _instance: "DBManager | None" = None

    def __new__(cls) -> "DBManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.settings = get_settings()
        self._tenants: Dict[str, str] = {}
        self.core_db_strategy = get_db_strategy(self.settings.CORE_DB_DRIVER)
        self.tenant_db_strategy = get_db_strategy(self.settings.TENANT_DB_DRIVER)

    async def init_core(self, *, generate_schemas: bool = False) -> None:
        if "default" in Tortoise._connections:
            return

        config = {
            "connections": {"default": self.settings.core_db_url},
            "apps": {
                "core_models": {
                    "models": ["adapters.database.core_models", "aerich.models"],
                    "default_connection": "default",
                },
            },
        }
        await Tortoise.init(config)
        if generate_schemas:
            await Tortoise.generate_schemas()

    async def init_tenant(
        self,
        tenant_id: str,
        *,
        db_url: Optional[str] = None,
        models: Optional[List[str]] = None,
        generate_schemas: bool = False,
    ) -> str:
        alias = f"tenant_{tenant_id}"
        if alias in Tortoise._connections:
            return alias

        await self.init_core()

        if not db_url:
            print(f"Generating DB URL for tenant {tenant_id}")
            db_url = await self.tenant_db_strategy.generate_db_url(
                tenant_id, self.settings
            )
            await self.tenant_db_strategy.create_db_if_needed(tenant_id, self.settings)

        config = {
            "connections": {
                "default": self.settings.core_db_url,
                alias: db_url,
            },
            "apps": {
                "core_models": {
                    "models": ["adapters.database.core_models", "aerich.models"],
                    "default_connection": "default",
                },
                "tenant_models": {
                    "models": models or ["adapters.database.tenant_models"],
                    "default_connection": alias,
                },
            },
        }

        await Tortoise.close_connections()
        await Tortoise.init(config)

        self._tenants[alias] = db_url
        if generate_schemas:
            await Tortoise.generate_schemas(safe=True)
        return alias


db_manager = DBManager()
