from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException
from .dependencies import SessionDep
# 
from src.db.database import engine
from src.models.models import User, Base
from src.schemas.users import NewUser
from src.exception import UserExistsException

user_router = APIRouter()

async def get_email_in_db(email: str, session: SessionDep):
    try:
        user = (await session.execute(select(User).filter_by(email=email))).one_or_none()
        if user:
            raise UserExistsException(email)
    except Exception as e:
        print('Ошибка с работой в базе')

async def add_user_in_db(user_for_add: NewUser, session: AsyncSession):
    try:
        await get_email_in_db(email=user_for_add.email, session=session)
        session.add(user_for_add)
        await session.commit()
    except Exception as e:
        print('Пользователь уже существует!')

    

# Регистрация пользователя
@user_router.post('/create-user')
async def create_user(new_user: NewUser, session: SessionDep):
    try:
        await add_user_in_db(new_user, session)
        return {'True': 'Пользователь побавлен'}
    except Exception as e:
        return {'message': f'Ошибка: {e}'}
    
@user_router.get('/create-database')
async def create_database():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            return {'True': 'База создана'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'{e}')

