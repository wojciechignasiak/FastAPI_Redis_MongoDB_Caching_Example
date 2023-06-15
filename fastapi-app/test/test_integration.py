import pytest
from app.models.software_developer import SoftwareDeveloperModel, UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import json
import asyncio

def test_create_software_developer(test_app, mongo_collection, redis_client):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    
    response = test_app.post("/fastapi-app/create-software-developer", json=jsonable_encoder(software_developer))
    assert response.status_code == 200
    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None

    mongo_data = mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(response[SoftwareDeveloperAttributes.mongo_id])})
    assert mongo_data is not None

    redis_data = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:{response[SoftwareDeveloperAttributes.mongo_id]}")
    assert redis_data is not None


def test_get_software_developer(test_app, mongo_collection, redis_client):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    response = test_app.post("/fastapi-app/create-software-developer", json=jsonable_encoder(software_developer))
    assert response.status_code == 200
    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None
    
    parameters = {"software_developer_id": response[SoftwareDeveloperAttributes.mongo_id]}
    response = test_app.get(f"/fastapi-app/get-software-developer", params=parameters)
    assert response.status_code == 200

    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None

    mongo_data = mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(response[SoftwareDeveloperAttributes.mongo_id])})
    print(mongo_data)
    assert mongo_data is not None

    redis_data = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:{response[SoftwareDeveloperAttributes.mongo_id]}")
    assert redis_data is not None


def test_update_software_developer(test_app, mongo_collection, redis_client):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@outlook.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    response = test_app.post("/fastapi-app/create-software-developer",
                                json=jsonable_encoder(software_developer))
    assert response.status_code == 200
    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None
    
    parameters = {"software_developer_id": response[SoftwareDeveloperAttributes.mongo_id]}
    updated_software_developer = UpdateSoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                                email="wojciech_ignasiak@gmail.com",
                                                                favourite_programming_language="Golang",
                                                                years_of_experience=1
    )
    response = test_app.patch(f"/fastapi-app/update-software-developer",
                            params=parameters,
                            json=jsonable_encoder(updated_software_developer))
    assert response.status_code == 200

    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None
    assert response[SoftwareDeveloperAttributes.email] == "wojciech_ignasiak@gmail.com"
    assert response[SoftwareDeveloperAttributes.favourite_programming_language] == "Golang"

    # mongo_data = mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(response[SoftwareDeveloperAttributes.mongo_id])})
    # assert mongo_data is not None
    # assert mongo_data[SoftwareDeveloperAttributes.email] == "wojciech_ignasiak@gmail.com"
    # assert mongo_data[SoftwareDeveloperAttributes.favourite_programming_language] == "Golang"

    redis_data = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:{response[SoftwareDeveloperAttributes.mongo_id]}")
    assert redis_data is not None
    redis_data = json.loads(redis_data)
    assert redis_data[SoftwareDeveloperAttributes.email] == "wojciech_ignasiak@gmail.com"
    assert redis_data[SoftwareDeveloperAttributes.favourite_programming_language] == "Golang"


def test_delete_software_developer(test_app, mongo_collection, redis_client):
    software_developer = SoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1)
    response = test_app.post("/fastapi-app/create-software-developer",
                                json=jsonable_encoder(software_developer))
    assert response.status_code == 200
    response = response.json()
    assert response[SoftwareDeveloperAttributes.mongo_id] is not None
    
    deleted_software_developer_id = response[SoftwareDeveloperAttributes.mongo_id]

    parameters = {"software_developer_id": response[SoftwareDeveloperAttributes.mongo_id]}
    response = test_app.delete(f"/fastapi-app/delete-software-developer",
                            params=parameters)
    assert response.status_code == 200

    # mongo_data = asyncio.run(mongo_collection.find_one({SoftwareDeveloperAttributes.mongo_id: ObjectId(deleted_software_developer_id)}))
    # assert mongo_data is None

    redis_data = redis_client.get(f"{SoftwareDeveloperAttributes.software_developer}:{deleted_software_developer_id}")
    assert redis_data is None