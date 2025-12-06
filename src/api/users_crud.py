import logging
from sqlalchemy import select
from fastapi import APIRouter, Response
from .dependencies import SessionDep
# 
from src.schemas.users_schemas import NewUser, UserData
from src.services.user_service import add_user_in_db, delete_user_by_db
# 
from src.models.models import Base
from src.db.database import engine

user_router = APIRouter(prefix='/users', tags=['Пользователи'])


@user_router.post('/create')
async def create_user(new_user: NewUser, session: SessionDep, response: Response):
    '''Регистрация пользователя'''

    resp = await add_user_in_db(new_user, session, response)
    return {'message': resp}


@user_router.delete('/delete-user-account')
async def delete_user_account(delete_user: UserData, session: SessionDep):
    '''Удаление всех данных о пользователе из бд''' 
    resp = await delete_user_by_db(delete_user, session)
    return {'message': resp}





@user_router.delete('/datadase')
async def database():
    '''Удалить этот энд поинт после работ !!!!!!!!'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)