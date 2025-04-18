from tortoise import fields
from tortoise.models import Model


class TenantUserModel(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "tenant_users"
        app = "tenant_models"
