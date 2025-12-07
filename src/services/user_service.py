import logging
from fastapi import HTTPException, status, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.services.auth import hashed_password, get_token_from_cookie
from src.models.models import User
from src.schemas.users_schemas import NewUser, UserData, ContactPhone
from src.services.auth import hashed_password, add_token, password_verification, update_verified_in_cookie
from src.exception import IsNotCorrectData, PhoneExists, TelegramExists

async def get_email_in_db(email: str, session: AsyncSession):
    '''Ищет пользователя в бд по email'''

    user = (await session.execute(select(User).filter_by(email=email))).scalar_one_or_none()
    return user

async def verification_user_data(user_email: str, user_password: str, response: Response, session: AsyncSession):
    try:
        if (user := await get_email_in_db(user_email, session)) and (await password_verification(user.password, user_password)):
            '''Создать токен и добавить в куку'''
            await add_token(user.name, user.email, user.role, user.verified, response)
            return 'Вы вошли в аккаунт'
        raise IsNotCorrectData
    except IsNotCorrectData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Данные не верны')
    except Exception as e:
        logging.warning(e)


async def add_user_in_db(user_for_add: NewUser, session: AsyncSession, response: Response):
    '''Добавляет пользователя (и добавление токе в куки) в бд если такой почты нет в бд'''

    user = await get_email_in_db(user_for_add.email, session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'Пользователь с почтой {user.email} уже существует')
    new_user = User(
            name=user_for_add.name,
            password=await hashed_password(user_for_add.password),
            email=user_for_add.email,
            role=user_for_add.role)
    try:
        session.add(new_user)
        await add_token(user_for_add.name, 
                        email=user_for_add.email, 
                        role=user_for_add.role, 
                        verified=False, response=response)
        await session.commit()
        return 'Пользователь добавлен'
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail='Пользователь не добавлен')


async def delete_user_by_db(user_for_delete: UserData, session: AsyncSession):
    '''Удаление пользователя из базы'''

    try:
        user = await get_email_in_db(user_for_delete.email, session)
        if user:
                if (await password_verification(db_password=user.password, user_password=user_for_delete.password)):
                    await session.delete(user)
                    await session.commit()
                    return 'Аккаунт пользователя удален'
        raise IsNotCorrectData
    except IsNotCorrectData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Данные не верны')
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail='Ошибка в работе базы данных')
    

async def get_user_by_token(request: Request, session: AsyncSession):
    token_data = await get_token_from_cookie(request)
    user = (await session.execute(select(User).filter_by(email=token_data.get('email')))).scalar_one()
    return user


async def add_phone_number_in_db(user_phone: str, request: Request, response: Response, session: AsyncSession):
    '''Добавление номера телефона в бд и смена статуса аккаунта'''

    try:
        if (user := await get_user_by_token(request, session)) and user.phone_number is None:
            user.phone_number = user_phone
            user.verified = True
            await update_verified_in_cookie(request, response)
            await session.commit()
            return 'Телефон добавлен'
        raise PhoneExists
    except PhoneExists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не можете сменить номер телефона')


async def add_telegram_in_db(telegram: str, request: Request, session: AsyncSession):
    '''Добавление телеграма в бд или замена уже существующего'''

    try:
        if (user := await get_user_by_token(request, session)):
            user.telegram = telegram
            await session.commit()
            return {'Телеграм добавлен'}
        raise TelegramExists
    except TelegramExists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не смогли сменить телеграм')



