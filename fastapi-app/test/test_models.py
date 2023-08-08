from app.models.software_developer import SoftwareDeveloperModel, UpdateSoftwareDeveloperModel, SoftwareDeveloperAttributes

def test_software_developer_model():
    software_developer = SoftwareDeveloperModel(id="abc",
                                                full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1
    )

    assert software_developer.id == "abc"
    assert software_developer.full_name == "Wojciech Ignasiak"
    assert software_developer.email == "wojciech_ignasiak@icloud.com"
    assert software_developer.favourite_programming_language == "Python"
    assert software_developer.years_of_experience == 1

def test_update_software_developer_model():
    software_developer = UpdateSoftwareDeveloperModel(full_name="Wojciech Ignasiak",
                                                email="wojciech_ignasiak@icloud.com",
                                                favourite_programming_language="Python",
                                                years_of_experience=1
    )

    assert software_developer.full_name == "Wojciech Ignasiak"
    assert software_developer.email == "wojciech_ignasiak@icloud.com"
    assert software_developer.favourite_programming_language == "Python"
    assert software_developer.years_of_experience == 1


def test_software_developer_attributes():
    assert SoftwareDeveloperAttributes.id == "id"
    assert SoftwareDeveloperAttributes.mongo_id == "_id"
    assert SoftwareDeveloperAttributes.full_name == "full_name"
    assert SoftwareDeveloperAttributes.email == "email"
    assert SoftwareDeveloperAttributes.favourite_programming_language == "favourite_programming_language"
    assert SoftwareDeveloperAttributes.years_of_experience == "years_of_experience"
    assert SoftwareDeveloperAttributes.software_developer == "software_developer"