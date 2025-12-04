from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# 
# from db.database import get_session
from src.db.database import get_session

# Зависимость: Создание Сессии
SessionDep = Annotated[AsyncSession, Depends(get_session)]