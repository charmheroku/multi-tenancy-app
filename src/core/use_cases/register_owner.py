from adapters.auth.security import hash_password
from core.domain.models import User
from core.repositories.user_repo import UserRepository


class RegisterOwner:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, email: str, password: str) -> User:
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        return await self.repo.create(email, hash_password(password), is_owner=True)
