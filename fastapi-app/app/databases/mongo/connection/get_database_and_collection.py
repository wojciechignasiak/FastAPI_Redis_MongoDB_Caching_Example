import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

async def get_database_and_collection(mongo_client: AsyncIOMotorClient) -> AsyncIOMotorCollection:
    try:
        mongo_db: AsyncIOMotorDatabase = mongo_client[MONGO_DB]
        mongo_collection: AsyncIOMotorCollection = mongo_db[MONGO_COLLECTION]
        return mongo_collection
    except Exception as e:
        print({"get_database_and_collection": f"Error: {e}"})
        