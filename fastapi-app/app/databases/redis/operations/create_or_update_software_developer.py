from app.models.software_developer import SoftwareDeveloperModel, SoftwareDeveloperAttributes
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
import redis
import json

async def create_or_update_software_developer_cache(redis_client: redis.Redis, created_or_updated_software_developer: SoftwareDeveloperModel) -> bool:
    try:
        result = redis_client.setex(f"{SoftwareDeveloperAttributes.software_developer}:"f"{created_or_updated_software_developer.id}", 10800, json.dumps(jsonable_encoder(created_or_updated_software_developer)))
        if result == True:
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"create_or_update_software_developer_cache": f"Error: {e}"}))