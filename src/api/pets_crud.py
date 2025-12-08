from fastapi import APIRouter, Response, Request
# 
from src.api.dependencies import SessionDep, AuthorizationCheckDep
from src.schemas.pets_schemas import (Pets, ChangeName, ChangeBreed, ChangeDescription,
                                      ChangePrice, ChangeLocation, Species)
from src.services.pet_service import (create_pet_for_sale, delete_user_pet_in_db,
                                      get_pet_by_id, update_name_pet_id_db, 
                                      update_breed_pet_id_db, update_description_pet_id_db,
                                      update_price_pet_id_db, update_location_pet_id_db,
                                      random_number)


dog_router = APIRouter(prefix='/dogs', tags=['Собаки'])

@dog_router.post('/create-pet')
async def create_dog(dog_for_add: Pets, auth: AuthorizationCheckDep, 
                     request: Request, session: SessionDep):
    '''Добавление собаки на продажу'''

    resp = await create_pet_for_sale(dog_for_add, request, session)
    return {'message': resp}


@dog_router.get('/{pet_id}')
async def get_pet(pet_id: int, session: SessionDep):
    '''Перейти на страницу животного'''

    resp = await get_pet_by_id(pet_id, session)
    return {'message': resp}


# @dog_router.post('/random-pet/{pet_id}')
@dog_router.post('/random-pet')
async def get_random_pet_id(species: Species, session: SessionDep):
    random_id = await random_number(species.species, session)
    resp = await get_pet_by_id(random_id, session)
    return {'message': resp}


@dog_router.patch('/{pet_id}/update-name')
async def change_name_in_pet(pet_id: int, new_name: ChangeName, 
                             request: Request, session: SessionDep):
    '''Сменить имя'''

    resp = await update_name_pet_id_db(pet_id, str(new_name.name), request, session)
    return {'message': resp}

@dog_router.patch('/{pet_id}/update-breed')
async def change_breed_in_pet(pet_id: int, new_breed: ChangeBreed, 
                             request: Request, session: SessionDep):
    '''Сменить породу'''

    resp = await update_breed_pet_id_db(pet_id, str(new_breed.breed), request, session)
    return {'message': resp}

@dog_router.patch('/{pet_id}/update-description')
async def change_description_in_pet(pet_id: int, new_description: ChangeDescription, 
                             request: Request, session: SessionDep):
    '''Сменить описание'''

    resp = await update_description_pet_id_db(pet_id, str(new_description.description), request, session)
    return {'message': resp}


@dog_router.patch('/{pet_id}/update-price')
async def change_price_in_pet(pet_id: int, new_price: ChangePrice, 
                             request: Request, session: SessionDep):
    '''Сменить цену'''

    resp = await update_price_pet_id_db(pet_id, new_price.price, request, session) #type: ignore
    return {'message': resp}


@dog_router.patch('/{pet_id}/update-location')
async def change_location_in_pet(pet_id: int, new_location: ChangeLocation, 
                             request: Request, session: SessionDep):
    '''Сменить локацию'''

    resp = await update_location_pet_id_db(pet_id, str(new_location.location), request, session)
    return {'message': resp}


@dog_router.delete('/{pet_id}/delete-pet')
async def delete_user_pet(pet_id: int, auth: AuthorizationCheckDep, request: Request, 
                          session: SessionDep):
    '''Удаление животного с продажи и из бд'''

    resp = await delete_user_pet_in_db(pet_id, request, session)
    return {'message': resp}




