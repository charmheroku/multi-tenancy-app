from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.core_auth import get_current_owner
from core.domain.models import User
from core.repositories.organization_repo import OrganizationRepository
from core.repositories.user_repo import UserRepository
from core.use_cases.create_organization import CreateOrganizationUseCase
from core.use_cases.login_owner import LoginOwner
from core.use_cases.register_owner import RegisterOwner

core_router = APIRouter(prefix="/api/core", tags=["Core"])


@core_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_owner(email: str, password: str):
    repo = UserRepository()
    try:
        user = await RegisterOwner(repo).execute(email, password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@core_router.post("/auth/login")
async def login_owner(email: str, password: str):
    repo = UserRepository()
    try:
        token = await LoginOwner(repo).execute(email, password)
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


@core_router.post("/organizations", status_code=status.HTTP_201_CREATED)
async def create_org(
    name: str,
    current_owner: User = Depends(get_current_owner),
):
    org_repo = OrganizationRepository()
    use_case = CreateOrganizationUseCase(org_repo, UserRepository())
    org = await use_case.execute(name=name, owner_id=current_owner.id)
    return {"id": org.id, "name": org.name, "db_url": org.db_url}
