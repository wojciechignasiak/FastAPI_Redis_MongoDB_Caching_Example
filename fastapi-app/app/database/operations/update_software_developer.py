from app.models.software_developer import UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes, SoftwareDeveloperModel
from motor.motor_asyncio import AsyncIOMotorCollection
from bson.objectid import ObjectId

async def update_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel):
    try:
        software_developer_document: dict = {
            SoftwareDeveloperAttributes.full_name: update_software_developer.full_name,
            SoftwareDeveloperAttributes.email: update_software_developer.email,
            SoftwareDeveloperAttributes.favourite_programming_language: update_software_developer.favourite_programming_language,
            SoftwareDeveloperAttributes.years_of_experience: update_software_developer.years_of_experience
        }
        updated_software_developer = await mongo_collection.find_one_and_update({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)}, {"$set": software_developer_document})
        updated_software_developer[SoftwareDeveloperAttributes.mongo_id] = str(updated_software_developer[SoftwareDeveloperAttributes.mongo_id])
        print(updated_software_developer)
        return SoftwareDeveloperModel.parse_obj(updated_software_developer)
    except Exception as e:
        print({"update_software_developer_query": f"Error: {e}"})