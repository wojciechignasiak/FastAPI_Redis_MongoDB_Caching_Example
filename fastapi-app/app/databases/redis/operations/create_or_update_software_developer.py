from app.models.software_developer import SoftwareDeveloperModel, SoftwareDeveloperAttributes
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
import redis
import json

async def create_or_update_software_developer_cache(redis_client: redis.Redis, updated_software_developer: SoftwareDeveloperModel):
    try:
        redis_client.setex(f"{SoftwareDeveloperAttributes.software_developer}:"f"{updated_software_developer.id}", 10800, json.dumps(jsonable_encoder(updated_software_developer)))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"create_or_update_software_developer_cache": f"Error: {e}"}))