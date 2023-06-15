from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.databases.mongo.operations.get_software_developer import get_software_developer_query
from app.models.software_developer import SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.get_software_developer import get_software_developer_cache
from app.databases.redis.operations.create_or_update_software_developer import create_or_update_software_developer_cache
import redis
import json

router = APIRouter()

@router.get("/get-software-developer", response_description="Get Software Developer")
async def get_software_developer_handler(software_developer_id: str, 
                                        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
                                        redis_client : redis.Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        software_developer = await get_software_developer_cache(redis_client, software_developer_id)
        if software_developer is not None:
            return JSONResponse(status_code=status.HTTP_200_OK,content=software_developer)
        else:
            mongo_database_and_collection = await get_database_and_collection(mongo_client)
            software_developer: SoftwareDeveloperModel = await get_software_developer_query(mongo_database_and_collection, software_developer_id)
            await create_or_update_software_developer_cache(redis_client, software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(software_developer))
    except HTTPException as e:
        raise e