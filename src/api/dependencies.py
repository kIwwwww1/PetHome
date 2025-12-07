from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.db.database import get_session
from src.services.auth import get_token_from_cookie

# Зависимость: Создание Сессии
SessionDep = Annotated[AsyncSession, Depends(get_session)]
AuthorizationCheckDep = Annotated[dict, Depends(get_token_from_cookie)]