from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.operations.delete_software_developer import delete_software_developer_query
from app.models.software_developer import SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.connection.get_mongo_client import get_mongo_client
from app.database.connection.get_database_and_collection import get_database_and_collection


router = APIRouter()

@router.delete("/delete-software-developer", response_description="Delete Software Developer")
async def delete_software_developer_handler(software_developer_id: str, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)) -> JSONResponse:
    try:
        mongo_database_and_collection = await get_database_and_collection(mongo_client)
        result: bool = await delete_software_developer_query(mongo_database_and_collection, software_developer_id)
        if result == False:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail=f"Software Developer with id: {software_developer_id} not found")
        else:
            return JSONResponse( status_code=status.HTTP_200_OK,content=f"Software Developer with id: {software_developer_id} deleted successfully")
    except HTTPException as e:
        raise e