from adapters.auth.security import hash_password
from tenant.domain.models import TenantUser
from tenant.repositories.user_repo import TenantUserRepository


class RegisterTenantUser:
    def __init__(self, repo: TenantUserRepository):
        self.repo = repo

    async def execute(self, email: str, password: str) -> TenantUser:
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        user = TenantUser(id=None, email=email, hashed_password=hash_password(password))
        return await self.repo.create(user)
