import os
import fakeredis.aioredis 

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",  # This is your local SQLite DB file
    },
    "apps": {
        "models": {
            "models": ["app.models.user", "app.models.quiz", "app.models.question"],
            "default_connection": "default",
        },
    },
}

async def init_redis():
    # Create a fake Redis connection
    return fakeredis.aioredis.FakeRedis(decode_responses=True)
