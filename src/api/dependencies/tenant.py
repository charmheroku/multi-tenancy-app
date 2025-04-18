from fastapi import Header, HTTPException
from adapters.database.core_models import OrganizationModel
from adapters.database.db_manager import db_manager
from tortoise.exceptions import OperationalError


async def get_tenant_alias(x_tenant: str | None = Header(default=None)) -> str:
    if not x_tenant:
        raise HTTPException(status_code=400, detail="X-TENANT header required")

    try:
        tenant_id = int(x_tenant)
        tenant = await OrganizationModel.get_or_none(id=tenant_id)

        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        return await db_manager.init_tenant(x_tenant, generate_schemas=True)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid tenant ID format")
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error initializing tenant: {str(e)}"
        )
