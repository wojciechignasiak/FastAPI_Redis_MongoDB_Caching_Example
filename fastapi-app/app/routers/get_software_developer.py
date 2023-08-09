from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.software_developer import SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.get_software_developer import get_software_developer_cache
from app.databases.redis.operations.create_or_update_software_developer import create_or_update_software_developer_cache
import redis
from app.databases.mongo.exceptions.mongo_exceptions import (DatabaseError, NotFoundError)
from app.databases.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager


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
            software_developer_query = SoftwareDeveloperQueryManager(mongo_database_and_collection)
            software_developer: SoftwareDeveloperModel = await software_developer_query.get(software_developer_id)
            await create_or_update_software_developer_cache(redis_client, software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(software_developer))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({e}))
    