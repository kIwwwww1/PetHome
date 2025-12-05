from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.models.models import User
from src.schemas.users_schemas import NewUser
from src.services.auth import hashed_password, add_token

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
        return {'True': 'Пользователь добавлен'}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail='Пользователь не добавлен')

        
        
