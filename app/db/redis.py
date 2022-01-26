from typing import Any

import aioredis

from app.core import settings


async def get_redis(redis, name: str) -> Any:
    return await redis.hgetall(name=name)


async def set_redis(redis, name: str, mapping: Any, expires: int) -> Any:
    await redis.hmset(name=name, mapping=mapping)
    await redis.expire(name=name, time=expires)


async def get_redis_pool() -> aioredis.Redis:
    return aioredis.from_url(
        settings.REDIS_URL,
        encoding='utf-8',
        decode_responses=True
    )
