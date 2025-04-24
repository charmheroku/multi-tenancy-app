from typing import Optional, Dict, Any

from tortoise import Tortoise
from tortoise.exceptions import OperationalError

from adapters.database.tenant_models import TenantUserModel
from tenant.domain.models import TenantUser


class TenantUserRepository:
    def __init__(self, alias: str) -> None:
        self.alias = alias
        self._updatable_fields = {"display_name", "email"}

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
            display_name=obj.display_name,
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
            display_name=obj.display_name,
        )

    async def create(self, user: TenantUser) -> TenantUser:
        if self.alias not in Tortoise._connections:
            raise OperationalError(f"Database {self.alias} not found")

        obj = await TenantUserModel.create(
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            display_name=user.display_name,
        )
        return TenantUser(
            id=obj.id,
            email=obj.email,
            hashed_password=obj.hashed_password,
            is_active=obj.is_active,
            display_name=obj.display_name,
        )

    async def update(self, user_id: int, data: Dict[str, Any]) -> Optional[TenantUser]:
        if self.alias not in Tortoise._connections:
            raise OperationalError(f"Database {self.alias} not found")

        user = await TenantUserModel.filter(id=user_id).first()
        if not user:
            return None

        filtered_data = {k: v for k, v in data.items() if k in self._updatable_fields}

        if filtered_data:
            for field, value in filtered_data.items():
                setattr(user, field, value)
            await user.save()

        return TenantUser(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            display_name=user.display_name,
        )
