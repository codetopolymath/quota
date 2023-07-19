from typing import Optional
from bson.objectid import ObjectId


from pydantic import BaseModel,  Field, EmailStr

class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class QuoteSchema(BaseModel):
    # Field(...) ---> ... from fields represent here field is required
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: str = Field(...)
    auther: str = Field(...)
    category: str = Field(...)
    tags: str = Field(...)
    created_at: str = Field(default="None", alias="created_at")
    updated_at: str = Field(default="None", alias="created_at")
   

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "know pain, feel pain, pain is everything",
                "auther": "madara uchiha",
                "category": "anime",
                "tags": "anime, madara uchiha",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01"
            }
        }

class UpdateQuoteModel(BaseModel):
    content : Optional[str]
    auther : Optional[str]
    category : Optional[str]
    tags : Optional[str]
    created_at : Optional[str]
    updated_at : Optional[str]


    class Config:
        schema_extra = {
            "example": {
                "content": "know pain, feel pain, pain is everything",
                "auther": "madara uchiha",
                "category": "anime",
                "tags": "anime, madara uchiha",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01"
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "message": message,
        "code": 200
    }

def ErrorResponseModel(error, message, code):
    return {
        "error": error,
        "message": message,
        "code": code
    }