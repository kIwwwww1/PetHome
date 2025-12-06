import logging
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.services.auth import hashed_password
from src.models.models import User
from src.schemas.users_schemas import NewUser, UserData
from src.services.auth import hashed_password, add_token, password_verification
from src.exception import IsNotCorrectData

async def get_email_in_db(email: str, session: AsyncSession):
    '''Ищет пользователя в бд по email'''

    user = (await session.execute(select(User).filter_by(email=email))).scalar_one_or_none()
    return user


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

