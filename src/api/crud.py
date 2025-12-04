from fastapi import APIRouter
from dependencies import SessionDep

user_router = APIRouter()

@user_router.post('/create-user')
async def create_user(new_user: ...):
    
