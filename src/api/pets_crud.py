from fastapi import APIRouter
# 
from src.api.dependencies import SessionDep, AuthorizationCheckDep
from src.schemas.pets_schemas import Pet


dog_router = APIRouter(prefix='/dogs', tags=['Собаки'])

@dog_router.post('/create')
async def create_dog(dog_for_add: Pet, auth: AuthorizationCheckDep, 
                     session: SessionDep):
    '''Добавление собаки на продажу'''
    pass





