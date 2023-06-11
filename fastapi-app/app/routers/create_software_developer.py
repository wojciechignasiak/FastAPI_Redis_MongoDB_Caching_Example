from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.operations.create_software_developer import create_software_developer_query
from app.models.software_developer import SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.connection.get_mongo_client import get_mongo_client
from app.database.connection.get_database_and_collection import get_database_and_collection


router = APIRouter()

@router.post("/create-software-developer", response_description="Create Software Developer")
async def create_software_developer_handler(software_developer: SoftwareDeveloperModel = Body(...), mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)) -> JSONResponse:
    try:        
        mongo_database_and_collection = await get_database_and_collection(mongo_client)
        created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_database_and_collection, software_developer)
        return JSONResponse( status_code=status.HTTP_200_OK,content=jsonable_encoder(created_software_developer) )
    except HTTPException as e:
        raise e
