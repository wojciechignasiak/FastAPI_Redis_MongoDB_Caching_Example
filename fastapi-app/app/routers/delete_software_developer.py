from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.models.mongo_collections import MongoCollections
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.mongo.exceptions.mongo_exceptions import (DatabaseError, NotFoundError)
from app.databases.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from redis import Redis
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.software_developer_cache_manager import SoftwareDeveloperCacheManager


router = APIRouter()

@router.delete("/delete-software-developer", response_description="Delete Software Developer")
async def delete_software_developer_handler(software_developer_id: str, 
                                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), 
                                            redis_client: Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_collection: AsyncIOMotorCollection = await get_database_and_collection(mongo_client, MongoCollections.software_developer)
        software_developer_query: SoftwareDeveloperQueryManager = SoftwareDeveloperQueryManager(mongo_collection)
        result: bool = await software_developer_query.delete(software_developer_id)
        if result == True:
            software_developer_cache: SoftwareDeveloperCacheManager = SoftwareDeveloperCacheManager(redis_client)
            await software_developer_cache.delete(software_developer_id)
            return JSONResponse(status_code=status.HTTP_200_OK,content=f"Software Developer with id: {software_developer_id} deleted successfully")
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str({e}))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    