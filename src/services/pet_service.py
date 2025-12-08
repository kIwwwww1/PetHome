import logging
from fastapi import HTTPException, status, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.models.models import Pet, PetPhoto
from src.schemas.pets_schemas import (Pets, ChangeName, ChangeBreed, ChangeDescription,
                                      ChangePrice, ChangeLocation)

from src.schemas.pets_schemas import Pets
from src.services.auth import get_token_from_cookie
from src.exception import PetNotFound


async def create_pet_for_sale(pet: Pets, request: Request, session: AsyncSession):
    '''создание и Добавление животного в бд'''

    session.add(Pet(
        name=pet.name,
        age=pet.age,
        breed=pet.breed,
        price=pet.price,
        description=pet.description,
        location=pet.location,
        owner_id=(await get_token_from_cookie(request))['id']
        
        ))
    await session.commit()
    return 'Пост успешно создан'


async def get_pet_by_id(id: int, session: AsyncSession):
    '''Поиск животного в базе по id'''

    try:
        pet = (await session.execute(select(Pet).filter_by(id=id))).scalar_one_or_none()
        if pet:
            return pet
        raise PetNotFound
    except PetNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Питомец не найден')


async def user_id_and_owner_id(pet_id: int, request: Request, session: AsyncSession):
    '''Проверяем у животного кто его владелец если совпадает пользователь и id владельца у животного 
    то возращаем животное'''

    pet = await get_pet_by_id(pet_id, session)
    _user_id = (await get_token_from_cookie(request))['id']
    if pet.owner_id == _user_id:
        return pet
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail='Вы не владелец')


async def delete_user_pet_in_db(pet_id: int, request: Request, session: AsyncSession):
    '''Убадение животного из базы и проверка на удаление'''

    pet_for_delete = await user_id_and_owner_id(pet_id, request, session)
    await session.delete(pet_for_delete)
    await session.commit()
    return 'Питомец удален'

async def update_name_pet_id_db(pet_id: int, new_name: str, 
                                request: Request, session: AsyncSession):
    pet_for_update = await user_id_and_owner_id(pet_id, request, session)
    if pet_for_update.name != new_name:
        pet_for_update.name = new_name
        await session.commit()
        return 'Вы сменили имя'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Не удалось сменить имя')

async def update_breed_pet_id_db(pet_id: int, new_breed: str, 
                                request: Request, session: AsyncSession):
    pet_for_update = await user_id_and_owner_id(pet_id, request, session)
    if pet_for_update.breed != new_breed:
        pet_for_update.breed = new_breed
        await session.commit()
        return 'Вы сменили породу'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Не удалось сменить породу')


async def update_description_pet_id_db(pet_id: int, new_description: str, 
                                request: Request, session: AsyncSession):
    pet_for_update = await user_id_and_owner_id(pet_id, request, session)
    if pet_for_update.description != new_description:
        pet_for_update.description = new_description
        await session.commit()
        return 'Вы сменили описание'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Не удалось сменить описание')

async def update_price_pet_id_db(pet_id: int, new_price: int, 
                                request: Request, session: AsyncSession):
    pet_for_update = await user_id_and_owner_id(pet_id, request, session)
    if pet_for_update.price != new_price:
        pet_for_update.price = new_price
        await session.commit()
        return 'Вы сменили цену'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Не удалось сменить цену')



async def update_location_pet_id_db(pet_id: int, new_location: str, 
                                request: Request, session: AsyncSession):
    pet_for_update = await user_id_and_owner_id(pet_id, request, session)
    if pet_for_update.location != new_location:
        pet_for_update.location = new_location
        await session.commit()
        return 'Вы сменили локацию'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Не удалось сменить локацию')

