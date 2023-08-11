from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.software_developer import SoftwareDeveloperModel, CreateSoftwareDeveloperModel
from app.models.mongo_collections import MongoCollections
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.databases.mongo.exceptions.mongo_exceptions import DatabaseError
from app.databases.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from redis import Redis
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.software_developer_cache_manager import SoftwareDeveloperCacheManager


router = APIRouter()

@router.post("/create-software-developer", response_description="Create Software Developer")
async def create_software_developer_handler(software_developer: CreateSoftwareDeveloperModel = Body(...), 
                                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), 
                                            redis_client: Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_collection: AsyncIOMotorCollection = await get_database_and_collection(mongo_client, MongoCollections.software_developer)
        software_developer_query: SoftwareDeveloperQueryManager = SoftwareDeveloperQueryManager(mongo_collection)
        created_software_developer: SoftwareDeveloperModel = await software_developer_query.create(software_developer)
        software_developer_cache: SoftwareDeveloperCacheManager = SoftwareDeveloperCacheManager(redis_client)
        cache_result: bool = await software_developer_cache.create_or_update(created_software_developer)
        if cache_result == True:
            return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(created_software_developer))
        else:
            await software_developer_cache.delete(created_software_developer.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(created_software_developer))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
