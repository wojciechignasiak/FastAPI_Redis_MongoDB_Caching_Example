from app.database.mongo.repositories.software_developer_repository_abc import SoftwareDeveloperRepositoryABC
from app.database.mongo.repositories.base_mongo_repository import BaseMongoRepository
from app.models.software_developer import (
    CreateSoftwareDeveloperModel, SoftwareDeveloperModel, 
    SoftwareDeveloperAttributes, UpdateSoftwareDeveloperModel
)
from app.database.mongo.exceptions.mongo_exceptions import (MongoDatabaseError, MongoNotFoundError)
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult, DeleteResult
from pymongo import ReturnDocument
from bson.objectid import ObjectId


class SoftwareDeveloperRepository(BaseMongoRepository, SoftwareDeveloperRepositoryABC):

    async def create(self, software_developer: CreateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        try:
            new_software_developer: InsertOneResult = await self.mongo_collection.insert_one(software_developer.model_dump())
            new_software_developer: dict = {SoftwareDeveloperAttributes.id.value: str(new_software_developer.inserted_id)}
            software_developer: dict = software_developer.model_dump()
            new_software_developer.update(software_developer)
            software_developer: SoftwareDeveloperModel = SoftwareDeveloperModel.model_validate(new_software_developer)
            return software_developer
        except MongoDatabaseError as e:
            raise MongoDatabaseError(f"SoftwareDeveloperRepository.create() error: {e}")

    async def delete(self, software_developer_id: str) -> bool:
        try:
            result: DeleteResult = await self.mongo_collection.delete_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
            if result.deleted_count == 1:
                return True
            else:
                raise MongoNotFoundError(f"SoftwareDeveloperRepository.delete() error: Software developer with id {software_developer_id} not found")
        except MongoNotFoundError as e:
            raise MongoNotFoundError(e)
        except MongoDatabaseError as e:
            raise MongoDatabaseError(f"SoftwareDeveloperQueryManager.delete() error: {e}")

    async def get(self, software_developer_id: str) -> SoftwareDeveloperModel:
        try:
            software_developer: dict = await self.mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)})
            if software_developer is None:
                raise MongoNotFoundError(f"SoftwareDeveloperRepository.get() error: Software developer with id {software_developer_id} not found")
            else:
                return SoftwareDeveloperModel.model_validate(software_developer)
        except MongoNotFoundError as e:
            raise MongoNotFoundError(e)
        except MongoDatabaseError as e:
            raise MongoDatabaseError(f"SoftwareDeveloperRepository.get() error: {e}")
        

    async def update(self, software_developer_id: str, update_software_developer: UpdateSoftwareDeveloperModel) -> SoftwareDeveloperModel:
        try:
            updated_software_developer: dict = await self.mongo_collection.find_one_and_update(
                {SoftwareDeveloperAttributes.mongo_id: ObjectId(software_developer_id)}, 
                {"$set": update_software_developer.remove_none_values_and_transform_to_dict()},
                return_document=ReturnDocument.AFTER
            )
            if updated_software_developer is None:
                raise MongoNotFoundError(f"SoftwareDeveloperRepository.update() error: Software developer with id {software_developer_id} not found")
            return SoftwareDeveloperModel.model_validate(updated_software_developer)
        except MongoNotFoundError as e:
            raise MongoNotFoundError(e)
        except MongoDatabaseError as e:
            raise MongoDatabaseError(f"SoftwareDeveloperRepository.update() error: {e}")
