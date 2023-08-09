from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.databases.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager
from app.models.software_developer import UpdateSoftwareDeveloperModel, SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.redis.connection.get_redis_client import get_redis_client
from app.databases.redis.operations.create_or_update_software_developer import create_or_update_software_developer_cache
import redis
from app.databases.mongo.exceptions.mongo_exceptions import DatabaseError

router = APIRouter()

@router.patch("/update-software-developer", response_description="Update Software Developer")
async def create_software_developer_handler(software_developer_id: str, 
                                            update_software_developer: UpdateSoftwareDeveloperModel = Body(...), 
                                            mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), 
                                            redis_client : redis.Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_database_and_collection = await get_database_and_collection(mongo_client)
        software_developer_query = SoftwareDeveloperQueryManager(mongo_database_and_collection)
        updated_software_developer: SoftwareDeveloperModel = await software_developer_query.update(software_developer_id, update_software_developer)
        await create_or_update_software_developer_cache(redis_client, updated_software_developer)
        return JSONResponse(status_code=status.HTTP_200_OK,content=jsonable_encoder(updated_software_developer))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"update_software_developer": f"Error: {e}"}))
