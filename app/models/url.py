from bson import ObjectId
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Optional
from .pyobject_id import PyObjectId
from models.database import db

collection = db['urls']
collection.create_index([('target_url', 1)])
VALIDITY_TIME = 1 # minutes


class UrlModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    key: str
    target_url : str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
        schema_extra = {
            "example": {
                "key": "xyz",
                "secret_key": "ABC123",
                "target_url" : "http://www.mobybit.it",
                "is_active": True,
                "clicks": 0,
                "created_at": datetime.now()
            }
        }

    def create_url(self):
        url = collection.insert_one(self.dict(by_alias=True))
        return {"url" : f"http://localhost:8000/{self.key}"}

    @staticmethod
    def get_original_url(key: str):
        return collection.find_one({"key": key})


    @staticmethod
    def get_url_by_target_url(target_url: str):
        return collection.find_one({"target_url": target_url})


    @staticmethod
    def check_url_validity(item):
        return item['created_at'] + timedelta(minutes=VALIDITY_TIME) > datetime.now()