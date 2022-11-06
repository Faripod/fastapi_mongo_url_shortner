
from fastapi import APIRouter, HTTPException, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import user as schemas
from models.user import UserModel
from app.utils.auth import verify_password, get_hashed_password
from app.utils.jwt import create_access_token


router = APIRouter(
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.UserAuth):
    new_user = UserModel(email=data.email, password=data.password)
    user_already_exist = new_user.create_user()
    if user_already_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")
    return {"detail" : "User created successfully"}


@router.post('/login', response_model=schemas.TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserModel.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    jwt_token = create_access_token(data={"sub": user['email']})

    return {"access_token" : jwt_token}
