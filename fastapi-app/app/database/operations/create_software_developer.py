from app.models.software_developer import SoftwareDeveloperModel, SoftwareDeveloperAttributes
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult


async def create_software_developer_query(mongo_collection: AsyncIOMotorCollection, software_developer: SoftwareDeveloperModel):
    try:
        software_developer_dict: dict = {
            SoftwareDeveloperAttributes.full_name: software_developer.full_name,
            SoftwareDeveloperAttributes.email: software_developer.email,
            SoftwareDeveloperAttributes.favourite_programming_language: software_developer.favourite_programming_language,
            SoftwareDeveloperAttributes.years_of_experience: software_developer.years_of_experience
        }
        new_software_developer: InsertOneResult = await mongo_collection.insert_one(software_developer_dict)
        # software_developer._id = new_software_developer.inserted_id
        software_developer.id = str(new_software_developer.inserted_id)
        return software_developer
    except Exception as e:
        print({"create_software_developer_query": f"Error: {e}"})