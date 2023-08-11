from app.models.software_developer import (
    CreateSoftwareDeveloperModel, SoftwareDeveloperModel, 
    SoftwareDeveloperAttributes, UpdateSoftwareDeveloperModel
)
from app.databases.mongo.exceptions.mongo_exceptions import (DatabaseError, NotFoundError)
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult, DeleteResult
from pymongo import ReturnDocument
from bson.objectid import ObjectId

class SoftwareDeveloperQueryManager:

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self.mongo_collection: AsyncIOMotorCollection = mongo_collection

    async def create(self, software_developer: CreateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        try:
            new_software_developer: InsertOneResult = await self.mongo_collection.insert_one(software_developer.model_dump())
            new_software_developer: dict = {SoftwareDeveloperAttributes.id.value: str(new_software_developer.inserted_id)}
            software_developer: dict = software_developer.model_dump()
            new_software_developer.update(software_developer)
            software_developer: SoftwareDeveloperModel = SoftwareDeveloperModel.model_validate(new_software_developer)
            return software_developer
        except DatabaseError as e:
            raise DatabaseError(f"create_software_developer: Error: {e}")

    async def delete(self, software_developer_id: str) -> bool:
        try:
            result: DeleteResult = await self.mongo_collection.delete_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
            if result.deleted_count == 1:
                return True
            else:
                raise NotFoundError(f"get_software_developer: Error: Software developer with id {software_developer_id} not found")
        except DatabaseError as e:
            raise DatabaseError(f"delete_software_developer: Error: {e}")

    async def get(self, software_developer_id: str) -> SoftwareDeveloperModel:
        try:
            software_developer: dict = await self.mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
            if software_developer is None:
                raise NotFoundError(f"get_software_developer: Error: Software developer with id {software_developer_id} not found")
            else:
                return SoftwareDeveloperModel.model_validate(software_developer)
        except DatabaseError as e:
            raise DatabaseError(f"get_software_developer: Error: {e}")

    async def update(self, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        try:
            updated_software_developer: dict = await self.mongo_collection.find_one_and_update(
                {SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)}, 
                {"$set": update_software_developer.model_dump()},
                return_document=ReturnDocument.AFTER
            )
            return SoftwareDeveloperModel.model_validate(updated_software_developer)
        except DatabaseError as e:
            raise DatabaseError(f"update_software_developer: Error: {e}")
