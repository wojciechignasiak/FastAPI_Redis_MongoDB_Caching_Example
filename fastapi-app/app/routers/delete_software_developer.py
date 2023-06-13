from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.databases.mongo.operations.delete_software_developer import delete_software_developer_query
from motor.motor_asyncio import AsyncIOMotorClient
from app.databases.mongo.connection.get_mongo_client import get_mongo_client
from app.databases.mongo.connection.get_database_and_collection import get_database_and_collection
from app.databases.redis.connection.get_redis_client import get_redis_client
import redis


router = APIRouter()

@router.delete("/delete-software-developer", response_description="Delete Software Developer")
async def delete_software_developer_handler(software_developer_id: str, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), redis_client : redis.Redis = Depends(get_redis_client)) -> JSONResponse:
    try:
        mongo_database_and_collection = await get_database_and_collection(mongo_client)
        result: bool = await delete_software_developer_query(mongo_database_and_collection, software_developer_id)
        if result == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Software Developer with id: {software_developer_id} not found")
        else:
            redis_client.delete("software_developer:"f"{software_developer_id}")
            return JSONResponse( status_code=status.HTTP_200_OK,content=f"Software Developer with id: {software_developer_id} deleted successfully")
    except HTTPException as e:
        raise e