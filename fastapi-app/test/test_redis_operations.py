import pytest
import redis
import json
from app.models.software_developer import SoftwareDeveloperModel, SoftwareDeveloperAttributes, CreateSoftwareDeveloperModel
from app.databases.redis.operations.create_or_update_software_developer import create_or_update_software_developer_cache
from app.databases.redis.operations.get_software_developer import get_software_developer_cache
from app.databases.redis.operations.delete_software_developer import delete_software_developer_cache


@pytest.mark.asyncio
async def test_create_or_update_software_developer_cache(redis_client: redis.Redis):
    mock_software_developer_id = "648b737eff5189b6b6ad9a84"
    software_developer = SoftwareDeveloperModel(id=mock_software_developer_id,
                                                full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)

    result = await create_or_update_software_developer_cache(redis_client, software_developer)
    assert result is True

    result = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:"f"{mock_software_developer_id}")
    assert result is not None

    result = json.loads(result)
    assert result["id"] == mock_software_developer_id

    software_developer = SoftwareDeveloperModel(id=mock_software_developer_id,
                                                full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Golang",
                                                years_of_experience=2)
    software_developer.id = mock_software_developer_id
    result = await create_or_update_software_developer_cache(redis_client, software_developer)
    assert result is True

    result = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:"f"{mock_software_developer_id}")
    assert result is not None
    result = json.loads(result)
    assert result["id"] == mock_software_developer_id
    assert result["favourite_programming_language"] == "Golang"
    assert result["years_of_experience"] == 2

@pytest.mark.asyncio
async def test_get_software_developer_cache(redis_client: redis.Redis):
    mock_software_developer_id = "648b737eff5189b6b6ad9a86"
    software_developer = SoftwareDeveloperModel(id=mock_software_developer_id,
                                                full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)

    result = await create_or_update_software_developer_cache(redis_client, software_developer)
    assert result is True

    result = await get_software_developer_cache(redis_client, mock_software_developer_id)
    assert result is not None
    assert result["id"] == mock_software_developer_id


@pytest.mark.asyncio
async def test_delete_software_developer_cache(redis_client: redis.Redis):
    mock_software_developer_id = "648b737eff5189b6b6ad9a87"
    software_developer = SoftwareDeveloperModel(id=mock_software_developer_id,
                                                full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)

    result = await create_or_update_software_developer_cache(redis_client, software_developer)
    assert result is True

    await delete_software_developer_cache(redis_client, mock_software_developer_id)


    result = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:"f"{mock_software_developer_id}")
    assert result is None

