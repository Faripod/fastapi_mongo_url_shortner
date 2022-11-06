from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from .pyobject_id import PyObjectId
from models.database import db
from app.utils.auth import get_hashed_password

collection = db['user']
collection.create_index([('email', 1)])


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
        schema_extra = {
            "example": {
                "email": "elfarinaawy@gmail.com",
                "password": "VeryS3cretPSW!",
            }
        }


    def create_user(self):
        user_already_exist = False
        user = collection.find_one({'email': self.email})
        if user:
            user_already_exist = True
        else:
            user = collection.insert_one({
                "email": self.email,
                "password": get_hashed_password(self.password)
                })


        return user_already_exist

    @classmethod
    def get_user(self):
        return collection.find_one({'email': self.email})


    @staticmethod
    def get_user_by_email(email: str):
        return collection.find_one({'email': email})