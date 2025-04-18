from settings import get_settings

settings = get_settings()

TORTOISE_ORM = {
    "connections": {"default": settings.core_db_url},
    "apps": {
        "core_models": {
            "models": ["adapters.database.core_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
