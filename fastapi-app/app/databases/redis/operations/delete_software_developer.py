from app.models.software_developer import SoftwareDeveloperAttributes
from fastapi import HTTPException, status
import redis


async def delete_software_developer_cache(redis_client: redis.Redis, software_developer_id: str):
    try:
        redis_client.delete(f"{SoftwareDeveloperAttributes.software_developer}:"f"{software_developer_id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str({"delete_software_developer_cache": f"Error: {e}"}))
