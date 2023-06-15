from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum

class SoftwareDeveloperModel(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    favourite_programming_language: str = Field(...)
    years_of_experience: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Wojciech Ignasiak",
                "email": "wojciech_ignasiak@icloud.com",
                "favourite_programming_language": "Python",
                "years_of_experience": 1,
            }
        }

class UpdateSoftwareDeveloperModel(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    favourite_programming_language: Optional[str]
    years_of_experience: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Wojciech Ignasiak",
                "email": "wojciech_ignasiak@outlook.com",
                "favourite_programming_language": "Python",
                "years_of_experience": 1,
            }
        }

class SoftwareDeveloperAttributes(str, Enum):
    id = 'id'
    mongo_id = '_id'
    full_name = 'full_name'
    email = 'email'
    favourite_programming_language = 'favourite_programming_language'
    years_of_experience = 'years_of_experience'
    software_developer = 'software_developer'