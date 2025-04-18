import uuid

from tortoise import Tortoise

from adapters.database.db_manager import db_manager
from core.domain.models import Organization
from core.repositories.organization_repo import OrganizationRepository
from core.repositories.user_repo import UserRepository


class CreateOrganizationUseCase:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        user_repo: UserRepository,
    ) -> None:
        self.org_repo = org_repo
        self.user_repo = user_repo

    async def execute(self, name: str, owner_id: int) -> Organization:
        await db_manager.init_core()

        user = await self.user_repo.get_by_id(owner_id)
        if not user or not user.is_owner:
            raise PermissionError("User is not allowed to create organization")

        org = await self.org_repo.create(
            name=name,
            owner_id=owner_id,
            db_url=f"tenant:{uuid.uuid4().hex[:8]}",
        )
        print(f"Organization created: {org.id}")

        await db_manager.init_tenant(
            tenant_id=str(org.id),
            generate_schemas=True,
        )

        if "default" not in Tortoise._connections:
            await db_manager.init_core()

        return org
