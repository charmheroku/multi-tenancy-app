from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.dependencies.tenant import get_tenant_alias
from settings import get_settings
from tenant.domain.models import TenantUser
from tenant.repositories.user_repo import TenantUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGO = "HS256"


async def get_current_tenant_user(
    token: str = Depends(oauth2_scheme),
    alias: str = Depends(get_tenant_alias),
) -> TenantUser:
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])

        if payload.get("scope") != "tenant":
            raise ValueError("Invalid token scope")

        user_id = int(payload["sub"])

        tenant_id = alias.split("_")[1] if "_" in alias else None

        if "tenant_id" not in payload:
            raise ValueError("Token must contain tenant_id")

        token_tenant_id = payload.get("tenant_id")
        if token_tenant_id != tenant_id:
            raise ValueError(
                f"Token tenant_id={token_tenant_id} "
                f"doesn't match requested tenant_id={tenant_id}"
            )

    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repo = TenantUserRepository(alias)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in this tenant",
        )
    return user
