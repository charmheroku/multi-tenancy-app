from tortoise import fields
from tortoise.models import Model


class CoreUserModel(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_owner = fields.BooleanField(default=False)

    class Meta:
        table = "core_users"
        app = "core_models"


class OrganizationModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    owner = fields.ForeignKeyField(
        "core_models.CoreUserModel", related_name="organizations"
    )
    db_url = fields.CharField(max_length=512)

    class Meta:
        table = "organizations"
        app = "core_models"
