from app.models.software_developer import SoftwareDeveloperAttributes
from fastapi import HTTPException, status
import redis
import json



async def get_software_developer_cache(redis_client: redis.Redis, software_developer_id: str):
    try:
        software_developer: bytes = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:"f"{software_developer_id}")
        if software_developer is not None:
            software_developer: str = software_developer.decode("utf-8")
            return json.loads(software_developer)
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"get_software_developer_cache": f"Error: {e}"}))
    