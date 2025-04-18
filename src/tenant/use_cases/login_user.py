from adapters.auth.jwt import create_access_token
from adapters.auth.security import verify_password
from tenant.repositories.user_repo import TenantUserRepository


class LoginTenantUser:
    def __init__(self, repo: TenantUserRepository):
        self.repo = repo

    async def execute(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        tenant_id = self.repo.alias.split("_")[1] if "_" in self.repo.alias else None

        token_data = {
            "sub": str(user.id),
            "scope": "tenant",
            "tenant_id": tenant_id,
        }
        return create_access_token(token_data)
