from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPassword, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDao
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDao.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDao.add_in_db(email=user_data.email, hashed_password=hashed_password)
    return 'User registered'


@router.post("/login")
async def login_user(responce: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user.id)})
    responce.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response,):
    response.delete_cookie("booking_access_token")
    return 'Logged out'

@router.get("/me")
async def read_users_me(current_user_data: Users = Depends(get_current_user)):
    return current_user_data


@router.get("/all_users")
async def read_users_all(current_user_data: Users = Depends(get_current_admin_user)):
    return await UsersDao.find_all()


