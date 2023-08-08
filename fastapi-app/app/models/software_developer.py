from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Any, Optional
from enum import Enum


class SoftwareDeveloperModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example":{
                "id": "648b737eff5189b6b6ad9a86",
                "full_name": "Wojciech Ignasiak",
                "email": "wojciech_ignasiak@outlook.com",
                "favourite_programming_language": "Python",
                "years_of_experience": 1
                }
            }
        )
    
    id: str = Field(...)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    favourite_programming_language: str = Field(...)
    years_of_experience: int = Field(...)

    @classmethod
    def model_validate(cls, data: dict) -> "SoftwareDeveloperModel":
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return super(SoftwareDeveloperModel, cls).model_validate(data)


class UpdateSoftwareDeveloperModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example":{
                "full_name": "Wojciech Ignasiak",
                "email": "wojciech_ignasiak@outlook.com",
                "favourite_programming_language": "Python",
                "years_of_experience": 1
                }
            }
        )
    full_name: Optional[str]
    email: Optional[EmailStr]
    favourite_programming_language: Optional[str]
    years_of_experience: Optional[int]


class CreateSoftwareDeveloperModel(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example":{
                "full_name": "Wojciech Ignasiak",
                "email": "wojciech_ignasiak@outlook.com",
                "favourite_programming_language": "Python",
                "years_of_experience": 1
                }
            }
        )
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    favourite_programming_language: str = Field(...)
    years_of_experience: int = Field(...)


class SoftwareDeveloperAttributes(str, Enum):
    id = 'id'
    mongo_id = '_id'
    full_name = 'full_name'
    email = 'email'
    favourite_programming_language = 'favourite_programming_language'
    years_of_experience = 'years_of_experience'
    software_developer = 'software_developer'