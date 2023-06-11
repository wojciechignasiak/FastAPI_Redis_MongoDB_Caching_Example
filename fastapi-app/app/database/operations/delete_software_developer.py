from bson.objectid import ObjectId
from pymongo.collection import Collection
from app.models.software_developer import SoftwareDeveloperAttributes
from pymongo.results import DeleteResult




async def delete_software_developer_query(collection: Collection, software_developer_id: str) -> bool:
    try:
        result: DeleteResult = await collection.delete_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
        if result.acknowledged == True:
            return True
        else:
            return False
    except Exception as e:
        print({"delete_software_developer_query": f"Error: {e}"})