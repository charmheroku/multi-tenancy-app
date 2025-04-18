from adapters.auth.jwt import create_access_token
from adapters.auth.security import verify_password
from core.repositories.user_repo import UserRepository


class LoginOwner:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if (
            not user
            or not verify_password(password, user.hashed_password)
            or not user.is_owner
        ):
            raise ValueError("Invalid credentials")
        token = create_access_token({"sub": str(user.id), "scope": "core"})
        return token
