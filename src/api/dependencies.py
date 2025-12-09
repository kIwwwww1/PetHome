from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.db.database import get_session
from src.services.auth import get_token_from_cookie
from src.services.admin_service import check_user_for_admin


SessionDep = Annotated[AsyncSession, Depends(get_session)]
AuthorizationCheckDep = Annotated[dict, Depends(get_token_from_cookie)]
AdminDep = Annotated[dict, Depends(check_user_for_admin)]