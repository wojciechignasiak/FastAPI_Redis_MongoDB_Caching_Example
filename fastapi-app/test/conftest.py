import pytest_asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorCollection
from app.database.redis.operations.software_developer_cache_manager import SoftwareDeveloperCacheManager
from app.database.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from app.main import app
from redis import Redis
from unittest.mock import Mock


@pytest_asyncio.fixture
def test_app():
    return TestClient(app)
    # with TestClient(app) as test_app:
    #     yield test_app  

@pytest_asyncio.fixture
async def mock_redis():
    return Mock(spec=Redis)

@pytest_asyncio.fixture
async def dev_cache_manager(mock_redis: Redis):
    return SoftwareDeveloperCacheManager(mock_redis)

@pytest_asyncio.fixture
async def mock_mongo_collection():
    return Mock(spec=AsyncIOMotorCollection)

@pytest_asyncio.fixture
async def dev_query_manager(mock_mongo_collection: AsyncIOMotorCollection):
    return SoftwareDeveloperQueryManager(mock_mongo_collection)