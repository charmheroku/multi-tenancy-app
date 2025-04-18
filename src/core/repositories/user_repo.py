from adapters.database.core_models import CoreUserModel
from core.domain.models import User


class UserRepository:
    async def create(self, email: str, hashed_password: str, is_owner: bool) -> User:
        obj = await CoreUserModel.create(
            email=email,
            hashed_password=hashed_password,
            is_owner=is_owner,
        )
        return User(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_owner=obj.is_owner,
        )

    async def get_by_id(self, user_id: int) -> User | None:
        obj = await CoreUserModel.get_or_none(id=user_id)
        if not obj:
            return None
        return User(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
            is_owner=obj.is_owner,
        )

    async def get_by_email(self, email: str) -> User | None:
        obj = await CoreUserModel.get_or_none(email=email)
        if not obj:
            return None
        return User(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
            is_owner=obj.is_owner,
        )
