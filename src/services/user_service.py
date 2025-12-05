from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import User
from src.schemas.users import NewUser

# Ищет пользователя в бд по email
async def get_email_in_db(email: str, session: AsyncSession):
    user = (await session.execute(select(User).filter_by(email=email))).scalar_one_or_none()
    return user

# Добавляет пользователя в бд если такой почты нет в бд
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
        
