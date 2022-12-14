import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Union
from models.user import UserModel
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({**data, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt

def decodeJWT(token: str) -> dict:
    try:
        print(token)
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        print(decoded_token['exp'])
        print(decoded_token['exp'] >= datetime.utcnow())
        return decoded_token if decoded_token['exp'] >= datetime.utcnow() else None
    except:
        return {}

def get_user_info_by_token(token: str):
    # remove bearer from token
    token = token[7:]
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token['username'], decoded_token['company']
    except:
        return None, None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = UserModel.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
