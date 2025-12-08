import logging
from fastapi import HTTPException, status, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# 
from src.models.models import Pet, PetPhoto
from src.schemas.pets_schemas import Pets
from src.services.auth import get_token_from_cookie


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

