import logging
from fastapi import HTTPException, status, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.models.models import Pet, PetPhoto
from src.schemas.pets_schemas import Pets
from src.services.auth import get_token_from_cookie
from src.exception import PetNotFound


async def create_pet_for_sale(pet: Pets, request: Request, session: AsyncSession):
    '''создание и Добавление животного в бд'''
    session.add(Pet(
        name=pet.name,
        age=pet.age,
        breed=pet.breed,
        description=pet.description,
        location=pet.location,
        owner_id=(await get_token_from_cookie(request))['id']
        
        ))
    await session.commit()
    return 'Пост успешно создан'

async def get_pet_by_id(id: int, session: AsyncSession):
    try:
        pet = (await session.execute(select(Pet).filter_by(id=id))).scalar_one_or_none()
        if pet:
            return pet
        raise PetNotFound
    except PetNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Питомец не найден')


async def user_id_and_owner_id(pet_id: int):
    pass


async def delete_user_pet_in_db(pet_id: int, session: AsyncSession):
    pet_for_delete = await get_pet_by_id(pet_id, session)
    await session.delete(pet_for_delete)
    await session.commit()
    return 'Питомец удален'


