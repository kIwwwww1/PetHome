import logging
from sqlalchemy import select
from fastapi import APIRouter, Response, Request
from .dependencies import (SessionDep, AdminDep)
# 
from src.schemas.users_schemas import NewUser, UserData, ContactPhone, ContactTelegram
from src.services.admin_service import (check_user_for_admin, create_admin, 
                                        delete_and_create_database, )
from src.services.auth import delete_token_from_cookie
from src.models.models import User


admin_router = APIRouter(prefix='/admin', tags=['Админы'])


@admin_router.get('/role_check')
async def check_user_role(is_admin: AdminDep, request: Request, 
                          session: SessionDep):
    '''Проверить своб роль'''

    resp = is_admin
    return {'message': resp}


@admin_router.post('create-admin/{user_id}')
async def create_new_admin(user_id: int, session: SessionDep):
    '''Сделать конкретного пользователя админом'''

    resp = await create_admin(user_id, session)
    return {'message': resp}


@admin_router.get('/delete-all-database')
async def delete_all_database(is_admin: AdminDep, session: SessionDep):
    '''Удаление и создание базы данных'''
    
    resp = await delete_and_create_database(session)
    return {'message': resp}
