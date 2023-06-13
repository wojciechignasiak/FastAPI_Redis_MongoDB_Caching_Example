from bson.objectid import ObjectId
from fastapi import HTTPException, status
from app.models.software_developer import SoftwareDeveloperAttributes
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import DeleteResult




async def delete_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer_id: str) -> bool:
    try:
        result: DeleteResult = await mongo_collection.delete_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
        if result.deleted_count == 1:
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"delete_software_developer_query": f"Error: {e}"}))
