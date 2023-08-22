import pytest
from unittest.mock import Mock
from app.models.software_developer import SoftwareDeveloperAttributes, SoftwareDeveloperModel
from app.database.redis.exceptions.redis_exceptions import RedisDatabaseError


@pytest.mark.asyncio
async def test_create_or_update_successful(mock_redis, dev_cache_manager):
    mock_software_dev = Mock(spec=SoftwareDeveloperModel, id="648b737eff5189b6b6ad9a86")
    mock_software_dev.id = "648b737eff5189b6b6ad9a86"
    mock_software_dev.model_dump_json.return_value = '{"full_name": "John Smith", "email": "john_smith@email.com", "favourite_programming_language": "Python", "years_of_experience": 1}'
    test: SoftwareDeveloperModel = SoftwareDeveloperModel
    test.model_fields
    mock_redis.setex.return_value = True

    result = await dev_cache_manager.create_or_update(mock_software_dev)

    assert result
    mock_redis.setex.assert_called_once_with(f"{SoftwareDeveloperAttributes.software_developer.value}:648b737eff5189b6b6ad9a86", 10800, '{"full_name": "John Smith", "email": "john_smith@email.com", "favourite_programming_language": "Python", "years_of_experience": 1}')

@pytest.mark.asyncio
async def test_create_or_update_failed(mock_redis, dev_cache_manager):
    mock_software_dev = Mock(spec=SoftwareDeveloperModel, id="648b737eff5189b6b6ad9a86")
    mock_redis.setex.return_value = False

    result = await dev_cache_manager.create_or_update(mock_software_dev)

    assert not result

@pytest.mark.asyncio
async def test_create_or_update_raises_exception(mock_redis, dev_cache_manager):
    mock_software_dev = Mock(spec=SoftwareDeveloperModel, id="648b737eff5189b6b6ad9a86")
    mock_redis.setex.side_effect = RedisDatabaseError("Error")

    with pytest.raises(RedisDatabaseError):
        await dev_cache_manager.create_or_update(mock_software_dev)

@pytest.mark.asyncio
async def test_get_found(mock_redis, dev_cache_manager):
    mock_redis.get.return_value = b'{"full_name": "John Smith", "email": "john_smith@email.com", "favourite_programming_language": "Python", "years_of_experience": 1}'

    result = await dev_cache_manager.get("648b737eff5189b6b6ad9a86")

    assert result == {"full_name": "John Smith", "email": "john_smith@email.com", "favourite_programming_language": "Python", "years_of_experience": 1}

@pytest.mark.asyncio
async def test_get_not_found(mock_redis, dev_cache_manager):
    mock_redis.get.return_value = None

    result = await dev_cache_manager.get("648b737eff5189b6b6ad9a86")

    assert result is None

@pytest.mark.asyncio
async def test_get_raises_exception(mock_redis, dev_cache_manager):
    mock_redis.get.side_effect = RedisDatabaseError("Error")

    with pytest.raises(RedisDatabaseError, match=r"SoftwareDeveloperCacheManager.get\(\) error: Error"):
        await dev_cache_manager.get("648b737eff5189b6b6ad9a86")

@pytest.mark.asyncio
async def test_delete(mock_redis, dev_cache_manager):

    await dev_cache_manager.delete("648b737eff5189b6b6ad9a86")
    mock_redis.delete.assert_called_once_with(f"{SoftwareDeveloperAttributes.software_developer.value}:648b737eff5189b6b6ad9a86")

@pytest.mark.asyncio
async def test_delete_raises_exception(mock_redis, dev_cache_manager):
    mock_redis.delete.side_effect = RedisDatabaseError("SoftwareDeveloperCacheManager.delete() error: Error")

    with pytest.raises(RedisDatabaseError, match=r"SoftwareDeveloperCacheManager.delete\(\) error: Error"):
        await dev_cache_manager.delete("648b737eff5189b6b6ad9a86")