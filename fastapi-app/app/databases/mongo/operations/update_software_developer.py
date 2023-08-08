from app.models.software_developer import UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes, SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from fastapi import HTTPException, status
from bson.objectid import ObjectId

async def update_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel):
    try:
        updated_software_developer: dict = await mongo_collection.find_one_and_update({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)}, 
                                                                                    {"$set": update_software_developer.model_dump()},
                                                                                    return_document=ReturnDocument.AFTER)
        return SoftwareDeveloperModel.model_validate(updated_software_developer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"update_software_developer_query": f"Error: {e}"}))
