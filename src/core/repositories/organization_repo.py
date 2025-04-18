from adapters.database.core_models import OrganizationModel
from core.domain.models import Organization


class OrganizationRepository:
    async def create(self, name: str, owner_id: int, db_url: str) -> Organization:
        obj = await OrganizationModel.create(
            name=name, owner_id=owner_id, db_url=db_url
        )
        return Organization(
            id=obj.id, name=obj.name, owner_id=obj.owner_id, db_url=obj.db_url
        )

    async def get_by_id(self, org_id: int) -> Organization | None:
        obj = await OrganizationModel.get_or_none(id=org_id)
        if not obj:
            return None
        return Organization(
            id=obj.id, name=obj.name, owner_id=obj.owner_id, db_url=obj.db_url
        )
