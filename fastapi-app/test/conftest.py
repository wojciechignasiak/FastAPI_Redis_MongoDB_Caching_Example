import pytest
import pytest_asyncio
import os
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from app.main import app
import redis



@pytest_asyncio.fixture
async def mongo_collection():
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_HOST = os.environ.get("MONGO_HOST")
    MONGO_PORT = os.environ.get("MONGO_PORT")
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

    print("Creating mongo client")
    mongo_client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
        )
    
    print("Dropping test database if exists")
    try:
        mongo_client.drop_database("test_db")
    except:
        pass

    mongo_db: AsyncIOMotorDatabase = mongo_client[MONGO_DB]
    mongo_collection: AsyncIOMotorCollection = mongo_db[MONGO_COLLECTION]

    yield mongo_collection

    print("Dropping test database")
    mongo_client.drop_database("test_db")

    print("Closing mongo client")
    mongo_client.close()


@pytest_asyncio.fixture
def redis_client():
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

    print("Creating redis client")
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    print("Flushing redis")
    try:
        redis_client.flushall()
    except:
        pass

    yield redis_client

    print("Flushing redis")
    redis_client.flushall()

    print("Closing redis client")
    redis_client.close()


@pytest.fixture(scope="module")
def test_app():
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_HOST = os.environ.get("MONGO_HOST")
    MONGO_PORT = os.environ.get("MONGO_PORT")
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

    with TestClient(app) as test_app:

        # startup event
        app.state.mongo_client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
        )

        app.state.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)  

        yield test_app  # dostarcza test_client do testu

        # shutdown event
        app.state.mongo_client.close()
        app.state.redis_client.close()