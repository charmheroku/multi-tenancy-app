from fastapi import FastAPI

from adapters.database.db_manager import db_manager
from api.routes.core import core_router
from api.routes.tenant import tenant_router

app = FastAPI(title="Multi‑Tenant App")

app.include_router(tenant_router, prefix="/api")
app.include_router(core_router, prefix="/api/core")


@app.on_event("startup")
async def on_startup() -> None:
    await db_manager.init_core(generate_schemas=True)
