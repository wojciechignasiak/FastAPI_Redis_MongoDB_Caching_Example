from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.software_developer import SoftwareDeveloperModel, CreateSoftwareDeveloperModel, UpdateSoftwareDeveloperModel
from app.models.mongo_collections import MongoCollections
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.database.mongo.exceptions.mongo_exceptions import MongoDatabaseError, MongoNotFoundError
from app.database.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from app.database.mongo.connection.get_mongo_client import get_mongo_client
from app.database.mongo.connection.get_database_and_collection import get_database_and_collection
from redis import Redis
from app.database.redis.exceptions.redis_exceptions import RedisDatabaseError
from app.database.redis.connection.get_redis_client import get_redis_client
from app.database.redis.operations.software_developer_cache_manager import SoftwareDeveloperCacheManager

router = APIRouter()

@router.post("/create-software-developer", response_description="Create Software Developer")
async def create_software_developer_endpoint(software_developer: CreateSoftwareDeveloperModel, 
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
    except MongoDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    except RedisDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))


@router.delete("/delete-software-developer", response_description="Delete Software Developer")
async def delete_software_developer_endpoint(software_developer_id: str, 
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
    except MongoNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str({e}))
    except MongoDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    except RedisDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))


@router.get("/get-software-developer", response_description="Get Software Developer")
async def get_software_developer_endpoint(software_developer_id: str, 
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
    except MongoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MongoDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    except RedisDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))


@router.patch("/update-software-developer", response_description="Update Software Developer")
async def create_software_developer_endpoint(software_developer_id: str, 
                                            update_software_developer: UpdateSoftwareDeveloperModel, 
                                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), 
                                            redis_client: Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_collection: AsyncIOMotorCollection = await get_database_and_collection(mongo_client, MongoCollections.software_developer)
        software_developer_query: SoftwareDeveloperQueryManager = SoftwareDeveloperQueryManager(mongo_collection)
        updated_software_developer: SoftwareDeveloperModel = await software_developer_query.update(software_developer_id, update_software_developer)
        software_developer_cache: SoftwareDeveloperCacheManager = SoftwareDeveloperCacheManager(redis_client)
        await software_developer_cache.create_or_update(updated_software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(updated_software_developer))
    except MongoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MongoDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    except RedisDatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))