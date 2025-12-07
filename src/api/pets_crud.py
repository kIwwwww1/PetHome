from fastapi import APIRouter, Response, Request
# 
from src.api.dependencies import SessionDep, AuthorizationCheckDep
from src.schemas.pets_schemas import Pets
from src.services.pet_service import create_pet_for_sale


dog_router = APIRouter(prefix='/dogs', tags=['Собаки'])

@dog_router.post('/create')
async def create_dog(dog_for_add: Pets, auth: AuthorizationCheckDep, 
                     request: Request, session: SessionDep):
    '''Добавление собаки на продажу'''
    resp = await create_pet_for_sale(dog_for_add, request, session)
    return {'message': resp}





