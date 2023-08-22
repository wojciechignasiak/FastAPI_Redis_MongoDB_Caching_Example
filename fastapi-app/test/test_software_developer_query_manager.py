import pytest
from bson.objectid import ObjectId
from unittest.mock import Mock, AsyncMock
from app.database.mongo.exceptions.mongo_exceptions import MongoDatabaseError, MongoNotFoundError
from app.models.software_developer import SoftwareDeveloperModel, CreateSoftwareDeveloperModel, UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes
from app.database.mongo.operations.software_developer_query_manager import SoftwareDeveloperQueryManager


@pytest.mark.asyncio
async def test_create_success(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev = CreateSoftwareDeveloperModel(full_name="John Smith", email="john_smith@email.com", favourite_programming_language="Python", years_of_experience=1)

    dev_query_manager.mongo_collection.insert_one = AsyncMock(return_value=Mock(inserted_id="648b737eff5189b6b6ad9a86"))

    result: SoftwareDeveloperModel = await dev_query_manager.create(mock_dev)

    assert result.id == "648b737eff5189b6b6ad9a86"
    assert result.full_name == "John Smith"
    assert result.favourite_programming_language == "Python"
    assert result.years_of_experience == 1

@pytest.mark.asyncio
async def test_create_failure(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev = CreateSoftwareDeveloperModel(full_name="John Smith", email="john_smith@email.com", favourite_programming_language="Python", years_of_experience=1)
    dev_query_manager.mongo_collection.insert_one = AsyncMock(side_effect=MongoDatabaseError("Error"))

    with pytest.raises(MongoDatabaseError, match=r"SoftwareDeveloperQueryManager.create\(\) error: Error"):
        await dev_query_manager.create(mock_dev)

@pytest.mark.asyncio
async def test_delete_success(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"

    dev_query_manager.mongo_collection.delete_one = AsyncMock(return_value=Mock(deleted_count=1))

    await dev_query_manager.delete(mock_dev_id)

    dev_query_manager.mongo_collection.delete_one.assert_called_once_with(
        {SoftwareDeveloperAttributes.mongo_id: ObjectId(mock_dev_id)}
    )

@pytest.mark.asyncio
async def test_delete_not_found_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    dev_query_manager.mongo_collection.delete_one = AsyncMock(side_effect=MongoNotFoundError(f"SoftwareDeveloperQueryManager.delete() error: Software developer with id {mock_dev_id} not found"))

    expected_message = f"SoftwareDeveloperQueryManager.delete() error: Software developer with id {mock_dev_id} not found"
    with pytest.raises(MongoNotFoundError) as exact_info:
        await dev_query_manager.delete(mock_dev_id)

        assert str(exact_info.value) == expected_message

@pytest.mark.asyncio
async def test_delete_database_error_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    dev_query_manager.mongo_collection.delete_one = AsyncMock(side_effect=MongoDatabaseError("Error"))

    with pytest.raises(MongoDatabaseError, match=r"SoftwareDeveloperQueryManager.delete\(\) error: Error"):
        await dev_query_manager.delete(mock_dev_id)

@pytest.mark.asyncio
async def test_get_success(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev = SoftwareDeveloperModel(id="648b737eff5189b6b6ad9a86",full_name="John Smith", email="john_smith@email.com", favourite_programming_language="Python", years_of_experience=1)
    dev_query_manager.mongo_collection.find_one = AsyncMock(return_value=mock_dev)

    result = await dev_query_manager.get(mock_dev.id)

    assert result == mock_dev

@pytest.mark.asyncio
async def test_get_not_found_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    dev_query_manager.mongo_collection.find_one = AsyncMock(side_effect=MongoNotFoundError(f"SoftwareDeveloperQueryManager.get() error: Software developer with id {mock_dev_id} not found"))

    expected_message = f"SoftwareDeveloperQueryManager.get() error: Software developer with id {mock_dev_id} not found"
    with pytest.raises(MongoNotFoundError) as exact_info:
        await dev_query_manager.get(mock_dev_id)

        assert str(exact_info.value) == expected_message

@pytest.mark.asyncio
async def test_get_database_error_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    dev_query_manager.mongo_collection.find_one = AsyncMock(side_effect=MongoDatabaseError("Error"))

    expected_message = f"SoftwareDeveloperQueryManager.get() error: Error"
    with pytest.raises(MongoDatabaseError) as exact_info:
        await dev_query_manager.get(mock_dev_id)

        assert str(exact_info.value) == expected_message

@pytest.mark.asyncio
async def test_update_success(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    mock_update_data = UpdateSoftwareDeveloperModel(full_name="Jane Doe", email="jane_doe@email.com")
    mock_returned_data = {
        "_id": ObjectId(mock_dev_id),
        "full_name": "Jane Doe",
        "email": "jane_doe@email.com",
        "favourite_programming_language": "Python",
        "years_of_experience": 5
    }

    dev_query_manager.mongo_collection.find_one_and_update = AsyncMock(return_value=mock_returned_data)

    result: SoftwareDeveloperModel = await dev_query_manager.update(mock_dev_id, mock_update_data)
    print(result)
    assert result.id == mock_dev_id
    assert result.full_name == "Jane Doe"

@pytest.mark.asyncio
async def test_update_not_found_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    mock_update_data = UpdateSoftwareDeveloperModel(full_name="Jane Doe", email="jane_doe@email.com")

    dev_query_manager.mongo_collection.find_one_and_update = AsyncMock(return_value=None)

    expected_message = f"SoftwareDeveloperQueryManager.update() error: Software developer with id {mock_dev_id} not found"
    with pytest.raises(MongoNotFoundError) as exact_info:
        await dev_query_manager.update(mock_dev_id, mock_update_data)
        assert str(exact_info.value) == expected_message

@pytest.mark.asyncio
async def test_update_database_error_exception(dev_query_manager: SoftwareDeveloperQueryManager):
    mock_dev_id = "648b737eff5189b6b6ad9a86"
    mock_update_data = UpdateSoftwareDeveloperModel(full_name="Jane Doe", email="jane_doe@email.com")
    dev_query_manager.mongo_collection.find_one_and_update = AsyncMock(side_effect=MongoDatabaseError("Database error"))

    expected_message = f"SoftwareDeveloperQueryManager.update() error: Database error"
    with pytest.raises(MongoDatabaseError) as exact_info:
        await dev_query_manager.update(mock_dev_id, mock_update_data)
        assert str(exact_info.value) == expected_message