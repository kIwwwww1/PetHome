import logging
from sqlalchemy import select
from fastapi import APIRouter, Response
from .dependencies import SessionDep
# 
from src.schemas.users_schemas import NewUser, UserData
from src.services.user_service import add_user_in_db, delete_user_by_db
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
async def login_account(user_data: UserData, session: SessionDep):
    pass



@user_router.get('/logout-account')
async def logout_user(response: Response, session: SessionDep):
    await delete_token_from_cookie(response)
    return {'message': 'Пользователь вышел из аккаунта'}

    


@user_router.delete('/delete-user-account')
async def delete_user_account(delete_user: UserData, session: SessionDep):
    '''Удаление всех данных о пользователе из бд''' 
    
    resp = await delete_user_by_db(delete_user, session)
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