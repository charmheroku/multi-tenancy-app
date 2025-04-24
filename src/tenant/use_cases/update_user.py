from typing import Dict, Any

from tenant.domain.models import TenantUser
from tenant.repositories.user_repo import TenantUserRepository


class UpdateTenantUser:
    """Use case for updating the tenant user profile."""

    def __init__(self, repository: TenantUserRepository) -> None:
        self.repository = repository

    async def execute(self, user_id: int, update_data: Dict[str, Any]) -> TenantUser:

        if not update_data:
            user = await self.repository.get_by_id(user_id)
            if not user:
                raise ValueError(f"User with id {user_id} not found")
            return user

        updated_user = await self.repository.update(user_id, update_data)
        if not updated_user:
            raise ValueError(f"User with id {user_id} not found")

        return updated_user
