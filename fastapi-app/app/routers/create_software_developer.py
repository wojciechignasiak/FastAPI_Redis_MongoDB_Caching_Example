from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.databases.mongo.operations.create_software_developer import create_software_developer_query
from app.models.software_developer import SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.create_or_update_software_developer import create_or_update_software_developer_cache
import redis

router = APIRouter()

@router.post("/create-software-developer", response_description="Create Software Developer")
async def create_software_developer_handler(software_developer: SoftwareDeveloperModel = Body(...), 
                                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), 
                                            redis_client: redis.Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_database_and_collection = await get_database_and_collection(mongo_client)
        created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_database_and_collection, software_developer)
        await create_or_update_software_developer_cache(redis_client, created_software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(created_software_developer) )
    except HTTPException as e:
        raise e
