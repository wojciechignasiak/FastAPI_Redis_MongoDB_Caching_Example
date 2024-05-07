from motor.motor_asyncio import AsyncIOMotorCollection


class BaseMongoRepository():

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self.mongo_collection: AsyncIOMotorCollection = mongo_collection