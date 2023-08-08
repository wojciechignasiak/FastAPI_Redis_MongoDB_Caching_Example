from app.models.software_developer import CreateSoftwareDeveloperModel, SoftwareDeveloperModel, SoftwareDeveloperAttributes
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult


async def create_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer: CreateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
    try:
        new_software_developer: InsertOneResult = await mongo_collection.insert_one(software_developer.model_dump())
        new_software_developer: dict = {SoftwareDeveloperAttributes.id.value: str(new_software_developer.inserted_id)}
        software_developer: dict = software_developer.model_dump()
        new_software_developer.update(software_developer)
        software_developer: SoftwareDeveloperModel = SoftwareDeveloperModel.model_validate(new_software_developer)
        return software_developer
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"create_software_developer_query": f"Error: {e}"}))