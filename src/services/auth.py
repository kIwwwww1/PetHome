import logging
import secrets
from fastapi import Response, Request, HTTPException, status
from os import getenv
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.hash import bcrypt
from jose import jwt, JWTError
# 
from src.exception import IsNotCorrectData

load_dotenv()

SECRET_KEY = str(getenv('SECRET_KEY'))
SECRET_ALGORITHM = str(getenv('ALGORITHM'))
COOKIES_SESSION_ID_KEY = str(getenv('COOKIES_SESSION_ID_KEY'))
THIRTY_DAYS = 30 * 24 * 60 * 60 

bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


async def create_access_token(id: int, name: str, email: str, role: str, verified: bool):
    '''Создание нового токена без добавления в куки'''

    encode = {'id': id, 'name': name, 'email': email, 'role': role, 'verified': verified}
    return jwt.encode(encode, SECRET_KEY, algorithm=SECRET_ALGORITHM)


async def add_token(id: int, name: str, email: str, role: str, verified: bool, response: Response):
    '''Создание токена и добавление в куки созданый токен'''

    token = await create_access_token(id, name, email, role, verified)
    response.set_cookie(key=COOKIES_SESSION_ID_KEY, value=token, max_age=THIRTY_DAYS, httponly=True, samesite='lax')
    return token


async def get_token_from_cookie(request: Request):
    '''Поиск токена в куках пользователя'''

    token = request.cookies.get(COOKIES_SESSION_ID_KEY)
    try:
        if not token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Вы не вошли в аккаунт')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECRET_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload


async def delete_token_from_cookie(response: Response):
    '''Удаление токена из кук если мы уверены что пользователь в аккаунте'''

    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    return 'Пользователь вышел из аккаунта'


async def update_verified_in_cookie(request: Request, response: Response):
    '''Пересоздание куки с новым статусом аккаунта'''

    cookie_token = await get_token_from_cookie(request)
    cookie_token['verified'] = True
    await add_token(**cookie_token, response=response)
    return 'Вы подтвердили аккаунт'


async def hashed_password(password: str) -> str:
    '''Хеширование пароля пользователя'''

    user_hashed_password = bcrypt_context.hash(password)
    return user_hashed_password


async def password_verification(db_password: str, user_password: str) -> bool:
    '''Сверка херированых паролей (из пароля и бд)'''

    return bcrypt_context.verify(user_password, db_password)
