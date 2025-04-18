from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.domain.models import User
from core.repositories.user_repo import UserRepository
from settings import Settings

oauth2_scheme_core = OAuth2PasswordBearer(tokenUrl="/api/core/auth/login")
ALGO = "HS256"


async def get_current_owner(token: str = Depends(oauth2_scheme_core)) -> User:
    try:
        payload = jwt.decode(token, Settings().JWT_SECRET, algorithms=[ALGO])
        if payload.get("scope") != "core":
            raise ValueError
        user_id = int(payload["sub"])
        print(f"Got user_id: {user_id}")
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    repo = UserRepository()
    user = await repo.get_by_id(user_id)
    if not user or not user.is_owner:
        raise HTTPException(status_code=403, detail="Not an owner")
    print(f"User: {user}")
    return user
