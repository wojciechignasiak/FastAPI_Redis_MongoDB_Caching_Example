from app.models.software_developer import SoftwareDeveloperModel, SoftwareDeveloperAttributes
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from bson.objectid import ObjectId



async def get_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer_id: str) -> SoftwareDeveloperModel:
    try:
        software_developer: dict = await mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
        if software_developer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str({"get_software_developer_query": f"Software developer with id {software_developer_id} not found"}))
        else:
            software_developer[SoftwareDeveloperAttributes.mongo_id] = str(software_developer[SoftwareDeveloperAttributes.mongo_id])
            return SoftwareDeveloperModel.parse_obj(software_developer)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"get_software_developer_query": f"Error: {e}"}))
    