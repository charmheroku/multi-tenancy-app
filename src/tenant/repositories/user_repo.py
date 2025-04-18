from typing import Optional

from tortoise import Tortoise
from tortoise.exceptions import OperationalError

from adapters.database.tenant_models import TenantUserModel
from tenant.domain.models import TenantUser


class TenantUserRepository:
    def __init__(self, alias: str) -> None:
        self.alias = alias

    async def get_by_email(self, email: str) -> Optional[TenantUser]:
        if self.alias not in Tortoise._connections:
            raise OperationalError(f"Database {self.alias} not found")

        obj = await TenantUserModel.filter(email=email).first()
        if not obj:
            return None
        return TenantUser(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
        )

    async def get_by_id(self, user_id: int) -> Optional[TenantUser]:
        if self.alias not in Tortoise._connections:
            raise OperationalError(f"Database {self.alias} not found")

        obj = await TenantUserModel.filter(id=user_id).first()
        if not obj:
            return None
        return TenantUser(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
        )

    async def create(self, user: TenantUser) -> TenantUser:
        if self.alias not in Tortoise._connections:
            raise OperationalError(f"Database {self.alias} not found")

        obj = await TenantUserModel.create(
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
        return TenantUser(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
        )
