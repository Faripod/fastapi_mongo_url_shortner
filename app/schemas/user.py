from pydantic import BaseModel

class UserAuth(BaseModel):
    email: str
    password: str

class TokenSchema(BaseModel):
    access_token: str