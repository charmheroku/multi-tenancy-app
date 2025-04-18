from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.auth import get_current_tenant_user
from api.dependencies.tenant import get_tenant_alias
from tenant.domain.models import TenantUser
from tenant.repositories.user_repo import TenantUserRepository
from tenant.use_cases.login_user import LoginTenantUser
from tenant.use_cases.register_user import RegisterTenantUser

tenant_router = APIRouter(tags=["Tenant"])


@tenant_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    email: str,
    password: str,
    alias: str = Depends(get_tenant_alias),
):
    try:
        repo = TenantUserRepository(alias)
        user = await RegisterTenantUser(repo).execute(email, password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@tenant_router.post("/auth/login")
async def login_user(
    email: str,
    password: str,
    alias: str = Depends(get_tenant_alias),
):
    try:
        repo = TenantUserRepository(alias)
        token = await LoginTenantUser(repo).execute(email, password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}",
        )


@tenant_router.get("/users/me")
async def read_profile(current: TenantUser = Depends(get_current_tenant_user)):
    return {"id": current.id, "email": current.email}
