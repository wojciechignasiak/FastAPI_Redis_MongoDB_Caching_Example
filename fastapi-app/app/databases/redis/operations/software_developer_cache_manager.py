from redis import Redis
from app.models.software_developer import SoftwareDeveloperAttributes, SoftwareDeveloperModel
from fastapi import HTTPException, status
import json


class SoftwareDeveloperCacheManager:

    def __init__(self, redis_client: Redis):
        self.redis_client: Redis = redis_client

    async def create_or_update(self, created_or_updated_software_developer: SoftwareDeveloperModel) -> bool:
        try:
            result = self.redis_client.setex(f"{SoftwareDeveloperAttributes.software_developer}:"f"{created_or_updated_software_developer.id}", 10800, created_or_updated_software_developer.model_dump_json())
            if result == True:
                return True
            else:
                return False
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"create_or_update_software_developer_cache": f"Error: {e}"}))

    async def get(self, software_developer_id: str):
        try:
            software_developer: bytes = self.redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:"f"{software_developer_id}")
            if software_developer is not None:
                software_developer: str = software_developer.decode("utf-8")
                return json.loads(software_developer)
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"get_software_developer_cache": f"Error: {e}"}))
    
    async def delete(self, software_developer_id: str):
        try:
            self.redis_client.delete(f"{SoftwareDeveloperAttributes.software_developer}:"f"{software_developer_id}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"delete_software_developer_cache": f"Error: {e}"}))