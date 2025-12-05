from typing import List
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default=f'User{id}')
    email: Mapped[str]
    role: Mapped[str] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    pets: Mapped[List['Pet']] = relationship('Pet', 
                                             back_populates='owner',
                                             cascade='all, delete-orphan',
                                             )

class Pet(Base):
    __tablename__ = 'pets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default='Без имени')
    age: Mapped[int] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(default='Беспородный')
    description: Mapped[str] = mapped_column(default='Описание отсутствует')
    location: Mapped[str] = mapped_column(default='Локация не указана')
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    owner: Mapped['User'] = relationship('User', back_populates='pets')
    photos: Mapped[List['PetPhoto']] = relationship('PetPhoto', 
                                                    back_populates='pet',
                                                    cascade='all, delete-orphan',
                                                    )

class PetPhoto(Base):
    __tablename__ = 'pet_photos'

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey('pets.id'), nullable=False)
    url: Mapped[str]
    order_index: Mapped[int]

    pet: Mapped['Pet'] = relationship('Pet', back_populates='photos')
    
