from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status
from .dependencies import SessionDep
# 
from src.db.database import engine
from src.models.models import User, Base
from src.schemas.users import NewUser
from src.exception import UserExistsException

user_router = APIRouter()


async def get_email_in_db(email: str, session: AsyncSession):
    user = (await session.execute(select(User).filter_by(email=email))).scalar_one_or_none()
    return user

async def add_user_in_db(user_for_add: NewUser, session: AsyncSession):
    user = await get_email_in_db(user_for_add.email, session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'Пользователь с почтой {user.email} уже существует')
    new_user = User(
            name=user_for_add.name,
            email=user_for_add.email,
            role=user_for_add.role
            )
    session.add(new_user)
    await session.commit()

    return 'Пользователь добавлен'
        

# Регистрация пользователя
@user_router.post('/create-user')
async def create_user(new_user: NewUser, session: SessionDep):
    resp = await add_user_in_db(new_user, session)
    return {'message': resp}


    

@user_router.get('/data')
async def get_all_data(session: SessionDep):
    try:
        return (await session.execute(select(User))).scalars().all()
    except Exception as e:
        return e
# @user_router.get('/create-database')
# async def create_database():
#     try:
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#             return {'True': 'База создана'}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=404, detail=f'{e}')

