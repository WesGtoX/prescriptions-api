from typing import Any

import aioredis

from fastapi import Request
from app.core import settings


async def get_redis(request: Request, name: str) -> Any:
    return await request.app.state.redis.hgetall(name=name)


async def set_redis(request: Request, name: str, mapping: Any, expires: int) -> Any:
    await request.app.state.redis.hmset(name=name, mapping=mapping)
    await request.app.state.redis.expire(name=name, time=expires)


async def get_redis_pool() -> aioredis.Redis:
    return aioredis.from_url(
        settings.REDIS_URL,
        encoding='utf-8',
        decode_responses=True
    )
