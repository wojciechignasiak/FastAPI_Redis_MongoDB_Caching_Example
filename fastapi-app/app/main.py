from fastapi import FastAPI
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from contextlib import asynccontextmanager
from redis import Redis
from app.routers import software_developer_router


MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialise databases clients.
    '''
    print("Starting fastapi-app app...")
    app.state.mongo_client = AsyncIOMotorClient(
        f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
        )
    
    while True:
        try:
            print("Testing connection to MongoDB...")
            mongo_info = await app.state.mongo_client.server_info()
            if mongo_info["ok"] == 1.0:
                print("Connection to MongoDB status: Connected")
            else:
                print("Connection to MongoDB status: Failed. Retrying...")
                raise ConnectionFailure
            break
        except ConnectionFailure:
            await asyncio.sleep(3)

    app.state.redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    while True:
        try:
            print("Testing connection to Redis...")
            redis_info = app.state.redis_client.ping()
            if redis_info:
                print('Connection to Redis status: Connected')
            else:
                print('Connection to Redis status: Failed. Retrying...')
                raise ConnectionError
            break
        except ConnectionError:
            await asyncio.sleep(3)

    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''
    print("Closing MongoDB Client...")
    app.state.mongo_client.close()

def create_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan, openapi_url="/fastapi-app/openapi.json", docs_url="/fastapi-app/docs")
    application.include_router(software_developer_router.router, prefix="/fastapi-app", tags=["fastapi-app"])
    return application

app = create_application()