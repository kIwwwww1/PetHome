from fastapi import APIRouter, Response, Request
# 
from src.api.dependencies import SessionDep, AuthorizationCheckDep
from src.schemas.pets_schemas import Pets
from src.services.pet_service import (create_pet_for_sale, delete_user_pet_in_db,
                                      get_pet_by_id)


dog_router = APIRouter(prefix='/dogs', tags=['Собаки'])

@dog_router.post('/create-pet')
async def create_dog(dog_for_add: Pets, auth: AuthorizationCheckDep, 
                     request: Request, session: SessionDep):
    '''Добавление собаки на продажу'''

    resp = await create_pet_for_sale(dog_for_add, request, session)
    return {'message': resp}


@dog_router.get('/pet/{pet_id}')
async def get_pet(pet_id: int, session: SessionDep):
    '''Перейти на строницу животного'''

    resp = await get_pet_by_id(pet_id, session)
    return {'message': resp}


@dog_router.delete('/delete-pet/{pet_id}')
async def delete_user_pet(pet_id: int, auth: AuthorizationCheckDep, request: Request, 
                          session: SessionDep):
    '''Удаление животного с продажи и из бд'''

    resp = await delete_user_pet_in_db(pet_id, request, session)
    return {'message': resp}




