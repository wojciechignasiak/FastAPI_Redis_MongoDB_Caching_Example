import pytest
from app.models.software_developer import SoftwareDeveloperModel, UpdateSoftwareDeveloperModel
from app.databases.mongo.operations.create_software_developer import create_software_developer_query
from app.databases.mongo.operations.get_software_developer import get_software_developer_query
from app.databases.mongo.operations.update_software_developer import update_software_developer_query
from app.databases.mongo.operations.delete_software_developer import delete_software_developer_query


@pytest.mark.asyncio
async def test_create_software_developer_query(mongo_collection):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_collection, software_developer)
    assert created_software_developer.id is not None



@pytest.mark.asyncio
async def test_get_software_developer_query(mongo_collection):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_collection, software_developer)
    assert created_software_developer.id is not None

    retrieved_software_developer: SoftwareDeveloperModel = await get_software_developer_query(mongo_collection, created_software_developer.id)
    assert retrieved_software_developer.id == created_software_developer.id


@pytest.mark.asyncio
async def test_update_software_developer_query(mongo_collection):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_collection, software_developer)
    assert created_software_developer.id is not None

    changed_software_developer = UpdateSoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Golang",
                                                years_of_experience=2)
    updated_software_developer: SoftwareDeveloperModel = await update_software_developer_query(mongo_collection, created_software_developer.id, changed_software_developer)
    assert updated_software_developer.id == created_software_developer.id
    assert updated_software_developer.favourite_programming_language == changed_software_developer.favourite_programming_language
    assert updated_software_developer.years_of_experience == changed_software_developer.years_of_experience


@pytest.mark.asyncio
async def test_delete_software_developer_query(mongo_collection):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    created_software_developer: SoftwareDeveloperModel = await create_software_developer_query(mongo_collection, software_developer)
    assert created_software_developer.id is not None
    
    result = await delete_software_developer_query(mongo_collection, created_software_developer.id)
    assert result is True





