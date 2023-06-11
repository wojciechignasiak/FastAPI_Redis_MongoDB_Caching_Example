from fastapi import FastAPI
import os
import asyncio
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure
from app.routers import (
    create_software_developer,
    delete_software_developer,
    update_software_developer
)
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")

def create_application() -> FastAPI:
    application = FastAPI(openapi_url="/fastapi-app/openapi.json", docs_url="/fastapi-app/docs")
    application.include_router(create_software_developer.router, prefix="/fastapi-app", tags=["fastapi-app"])
    application.include_router(delete_software_developer.router, prefix="/fastapi-app", tags=["fastapi-app"])
    application.include_router(update_software_developer.router, prefix="/fastapi-app", tags=["fastapi-app"])
    return application

app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting fastapi-app app...")
    app.state.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
        )
    
    while True:
        try:
            print("Testing connection to MongoDB...")
            server_info = await app.state.mongo_client.server_info()
            if server_info["ok"] == 1.0:
                print("Connection to MongoDB status: Connected")
            else:
                print("Connection to MongoDB status: Failed. Retrying...")
                raise ConnectionFailure
            break
        except ConnectionFailure:
            await asyncio.sleep(3)

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting fastapi-app app down...")
    app.state.mongo_client.close()