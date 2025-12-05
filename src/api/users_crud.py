from sqlalchemy import select
from fastapi import APIRouter
from .dependencies import SessionDep
# 
from src.schemas.users import NewUser
from src.services.user_service import add_user_in_db

user_router = APIRouter(prefix='/users', tags=['Пользователи'])

user_tag = 'Пользователь'

# Регистрация пользователя
@user_router.post('/create')
async def create_user(new_user: NewUser, session: SessionDep):
    resp = await add_user_in_db(new_user, session)
    return {'message': resp}

# @user_router.delete('')