"""FastAPI dependency that guarantees tenant DB connection."""

from fastapi import Header, HTTPException

from adapters.database.db_manager import db_manager


async def get_tenant_alias(x_tenant: str | None = Header(default=None)) -> str:
    if not x_tenant:
        raise HTTPException(status_code=400, detail="X-TENANT header required")

    return await db_manager.init_tenant(x_tenant)
