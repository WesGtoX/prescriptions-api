import time
import pytest

from app.db.redis import get_redis, set_redis


@pytest.mark.asyncio
async def test_get_redis(redis) -> None:
    name, mapping = 'foo', {'bar': 1}
    await redis.hmset(name, mapping)
    assert await get_redis(redis, name) == {'bar': '1'}


@pytest.mark.asyncio
async def test_set_redis(redis) -> None:
    name, mapping, expires = 'bar', {'foo': 2}, 3600
    assert await redis.hgetall(name) == {}
    await set_redis(redis, name, mapping, expires)
    assert await redis.hgetall(name) == {'foo': '2'}


@pytest.mark.asyncio
async def test_redis_expires(redis) -> None:
    name, mapping, expires = 'fizz', {'buzz': 3}, 1
    await set_redis(redis, name, mapping, expires)
    assert await redis.hgetall(name) == {'buzz': '3'}
    time.sleep(1)
    assert await redis.hgetall(name) == {}
