import logging
from sqlalchemy import select
from fastapi import APIRouter, Response, Request
from .dependencies import SessionDep
# 
from src.schemas.users_schemas import NewUser, UserData, ContactPhone, ContactTelegram
from src.services.user_service import (add_user_in_db, delete_user_by_db, 
                                       verification_user_data, add_phone_number_in_db,
                                       add_telegram_in_db)
from src.services.auth import delete_token_from_cookie
# 
from src.models.models import User
from src.models.models import Base
from src.db.database import engine

user_router = APIRouter(prefix='/users', tags=['Пользователи'])


@user_router.post('/create-account')
async def create_user(new_user: NewUser, session: SessionDep, response: Response):
    '''Регистрация пользователя'''

    resp = await add_user_in_db(new_user, session, response)
    return {'message': resp}


@user_router.post('/login-account')
async def login_account(user_data: UserData, response: Response, session: SessionDep):
    resp = await verification_user_data(user_data.email, user_data.password, response, session)
    return {'message': resp}


@user_router.get('/logout-account')
async def logout_user(response: Response, session: SessionDep):
    resp = await delete_token_from_cookie(response)
    return {'message': resp}


@user_router.delete('/delete-user-account')
async def delete_user_account(delete_user: UserData, session: SessionDep):
    '''Удаление всех данных о пользователе из бд''' 
    
    resp = await delete_user_by_db(delete_user, session)
    return {'message': resp}


@user_router.post('/add-contacts/phone-number')
async def add_user_phone_number(user_phone: ContactPhone, request: Request, response: Response, session: SessionDep):
    resp = await add_phone_number_in_db(user_phone.phone, request, response, session)
    return {'message': resp}


@user_router.post('/add-contacts/telegram')
async def add_user_telegram(user_telegram: ContactTelegram, request: Request, session: SessionDep):
    resp = await add_telegram_in_db(user_telegram.telegram, request, session)
    return {'message': resp}











@user_router.delete('/delete-all-users')
async def delete_all_users(session: SessionDep):
    '''Удалить все пользователй Удалить этот энд поинт после работ !!!!!!!!'''

    users = (await session.execute(select(User))).scalars().all()
    logging.info(users)
    for user in users:
        await session.delete(user)
    await session.commit()
    return {'message': 'Все пользователи удалены'}



@user_router.delete('/datadase')
async def database():
    '''Удалить этот энд поинт после работ !!!!!!!!'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)