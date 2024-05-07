from starlette.requests import Request
from motor.motor_asyncio import AsyncIOMotorClient


async def get_mongo_client(request: Request) -> AsyncIOMotorClient:
    try:
        return request.app.state.mongo_client
    except Exception as e:
        print({"get_mongo_client": f"Error: {e}"})