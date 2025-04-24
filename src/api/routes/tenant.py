from fastapi import APIRouter, Depends, HTTPException, Body, status

from api.dependencies.auth import get_current_tenant_user
from api.dependencies.tenant import get_tenant_alias
from api.schemas.tenant import (
    TenantUserCreate,
    TenantUserLogin,
    TenantUserResponse,
    TenantUserUpdate,
    TokenResponse,
)
from tenant.domain.models import TenantUser
from tenant.repositories.user_repo import TenantUserRepository
from tenant.use_cases.login_user import LoginTenantUser
from tenant.use_cases.register_user import RegisterTenantUser
from tenant.use_cases.update_user import UpdateTenantUser
from tortoise.exceptions import OperationalError

tenant_router = APIRouter(tags=["Tenant"])


@tenant_router.post(
    "/auth/register",
    response_model=TenantUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: TenantUserCreate,
    alias: str = Depends(get_tenant_alias),
):
    try:
        repo = TenantUserRepository(alias)
        user = await RegisterTenantUser(repo).execute(
            user_data.email, user_data.password
        )
        return TenantUserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            is_active=user.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}",
        )


@tenant_router.post("/auth/login", response_model=TokenResponse)
async def login_user(
    credentials: TenantUserLogin,
    alias: str = Depends(get_tenant_alias),
):
    try:
        repo = TenantUserRepository(alias)
        token = await LoginTenantUser(repo).execute(
            credentials.email, credentials.password
        )
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}",
        )


@tenant_router.get("/users/me", response_model=TenantUserResponse)
async def read_profile(current: TenantUser = Depends(get_current_tenant_user)):
    return TenantUserResponse(
        id=current.id,
        email=current.email,
        display_name=current.display_name,
        is_active=current.is_active,
    )


@tenant_router.put("/users/me", response_model=TenantUserResponse)
async def update_profile(
    update_data: TenantUserUpdate = Body(...),
    current: TenantUser = Depends(get_current_tenant_user),
    alias: str = Depends(get_tenant_alias),
):
    try:
        repo = TenantUserRepository(alias)
        use_case = UpdateTenantUser(repo)

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

        updated_user = await use_case.execute(current.id, update_dict)

        return TenantUserResponse(
            id=updated_user.id,
            email=updated_user.email,
            display_name=updated_user.display_name,
            is_active=updated_user.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}",
        )
