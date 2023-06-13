from app.models.software_developer import UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes, SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from fastapi import HTTPException, status
from bson.objectid import ObjectId

async def update_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel):
    try:
        software_developer_document: dict = {
            SoftwareDeveloperAttributes.full_name: update_software_developer.full_name,
            SoftwareDeveloperAttributes.email: update_software_developer.email,
            SoftwareDeveloperAttributes.favourite_programming_language: update_software_developer.favourite_programming_language,
            SoftwareDeveloperAttributes.years_of_experience: update_software_developer.years_of_experience
        }
        updated_software_developer: dict = await mongo_collection.find_one_and_update({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)}, 
                                                                                    {"$set": software_developer_document},
                                                                                    return_document=ReturnDocument.AFTER)
        updated_software_developer[SoftwareDeveloperAttributes.mongo_id] = str(updated_software_developer[SoftwareDeveloperAttributes.mongo_id])
        return SoftwareDeveloperModel.parse_obj(updated_software_developer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"update_software_developer_query": f"Error: {e}"}))
