import pytest
import fakeredis.aioredis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from starlette.testclient import TestClient

from app.main import app
from app.db.database import Base
from app.dependencies import get_db

engine = create_engine('sqlite:///./test.db', connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db() -> None:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def fake_server(request) -> fakeredis.FakeServer:
    server = fakeredis.FakeServer()
    server.connected = request.node.get_closest_marker('disconnected') is None
    return server


@pytest.fixture(params=[pytest.param('fake', marks=pytest.mark.fake)])
async def redis(request) -> None:
    fake_server = request.getfixturevalue('fake_server')
    ret = fakeredis.aioredis.FakeRedis(server=fake_server, encoding='utf-8', decode_responses=True)

    if not fake_server or fake_server.connected:
        await ret.flushall()

    yield ret

    if not fake_server or fake_server.connected:
        await ret.flushall()
    await ret.connection_pool.disconnect()


@pytest.fixture(autouse=True)
def test_client(redis) -> None:
    with TestClient(app) as test_client:
        app.state.redis = redis
        yield test_client
