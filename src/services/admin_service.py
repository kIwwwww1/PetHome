import logging
from fastapi import HTTPException, status, Response, Request
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.services.auth import hashed_password, get_token_from_cookie
from src.models.models import User
from src.schemas.users_schemas import NewUser, UserData, ContactPhone
from src.services.auth import (hashed_password, add_token, 
                               password_verification, update_verified_in_cookie,
                               delete_token_from_cookie)
from src.services.pet_service import get_pet_by_id
from src.exception import (IsNotCorrectData, PhoneExists, 
                           TelegramExists, UserIsNotAdmin)
from src.models.models import Base
from src.db.database import engine


async def check_user_for_admin(request: Request):
    '''Проверка роли пользователя'''

    token_data = await get_token_from_cookie(request)
    logging.info(token_data)
    try:
        if token_data['role'] == 'admin':
            return token_data
        raise UserIsNotAdmin
    except UserIsNotAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вы не админ')


async def get_user_by_id(user_id: int, session: AsyncSession):
    '''Найти пользователя по id'''

    try:
        user = (await session.execute(select(User).filter_by(id=user_id))).scalar_one_or_none()
        if user:
            return user
        raise IsNotCorrectData
    except IsNotCorrectData:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не нашли пользователя')


async def create_admin(id: int, session: AsyncSession):
    '''Сделать пользователя админом'''

    user = await get_user_by_id(id, session)
    user.role = 'admin'
    await session.commit()
    return 'Вы сделали пользователя админом'


async def delete_user_accunt_by_id(id: int, session: AsyncSession):
    '''Удаление пользователя по id'''

    user = await get_user_by_id(id, session)
    await session.delete(user)
    await session.commit()
    return 'Пользователь удален'


async def delete_user_pet_by_id(pet_id: int, session: AsyncSession):
    '''Удаление животного у пользователя по id питомца'''

    pet_for_delete = await get_pet_by_id(pet_id, session)
    await session.delete(pet_for_delete)
    await session.commit()
    return 'Питомец удален'




async def delete_and_create_database(sesison: AsyncSession):
    '''Удаление и создание базы данных'''

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return 'База пересоздана'

