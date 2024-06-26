from app.database.redis.repositories.base_redis_repository import BaseRedisRepository
from app.database.redis.repositories.software_developer_cache_repository_abc import SoftwareDeveloperCacheRepositoryABC
from app.models.software_developer import SoftwareDeveloperAttributes, SoftwareDeveloperModel
from app.database.redis.exceptions.redis_exceptions import RedisDatabaseError
import json


class SoftwareDeveloperCacheRepository(BaseRedisRepository, SoftwareDeveloperCacheRepositoryABC):

    async def create_or_update(self, created_or_updated_software_developer: SoftwareDeveloperModel) -> bool:
        try:
            result = self.redis_client.setex(f"{SoftwareDeveloperAttributes.software_developer.value}:"f"{created_or_updated_software_developer.id}", 10800, created_or_updated_software_developer.model_dump_json())
            if result == True:
                return True
            else:
                return False
        except RedisDatabaseError as e:
            raise RedisDatabaseError(f"SoftwareDeveloperCacheRepository.create_or_update() error: {e}")

    async def get(self, software_developer_id: str) -> dict|None:
        try:
            software_developer: bytes = self.redis_client.get(f"{SoftwareDeveloperAttributes.software_developer.value}:"f"{software_developer_id}")
            if software_developer is not None:
                software_developer: str = software_developer.decode("utf-8")
                return json.loads(software_developer)
            else:
                return None
        except RedisDatabaseError as e:
            raise RedisDatabaseError(f"SoftwareDeveloperCacheRepository.get() error: {e}")
    
    async def delete(self, software_developer_id: str):
        try:
            self.redis_client.delete(f"{SoftwareDeveloperAttributes.software_developer.value}:"f"{software_developer_id}")
        except RedisDatabaseError as e:
            raise RedisDatabaseError(f"SoftwareDeveloperCacheRepository.delete() error: {e}")