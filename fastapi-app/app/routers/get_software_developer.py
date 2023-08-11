from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.models.mongo_collections import MongoCollections
from app.models.software_developer import SoftwareDeveloperModel
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.mongo.exceptions.mongo_exceptions import (DatabaseError, NotFoundError)
from app.databases.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from redis import Redis
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.software_developer_cache_manager import SoftwareDeveloperCacheManager

router = APIRouter()

@router.get("/get-software-developer", response_description="Get Software Developer")
async def get_software_developer_handler(software_developer_id: str, 
                                        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
                                        redis_client: Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        software_developer_cache: SoftwareDeveloperCacheManager = SoftwareDeveloperCacheManager(redis_client)
        software_developer = await software_developer_cache.get(software_developer_id)
        if software_developer is not None:
            return JSONResponse(status_code=status.HTTP_200_OK,content=software_developer)
        else:
            mongo_collection: AsyncIOMotorCollection = await get_database_and_collection(mongo_client, MongoCollections.software_developer)
            software_developer_query: SoftwareDeveloperQueryManager = SoftwareDeveloperQueryManager(mongo_collection)
            software_developer: SoftwareDeveloperModel = await software_developer_query.get(software_developer_id)
            await software_developer_cache.create_or_update(software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(software_developer))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    