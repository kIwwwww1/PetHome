from typing import List, Annotated
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default=f'User{id}')
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    telegram: Mapped[str] = mapped_column(nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
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
    species: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str]
    age: Mapped[int] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(index=True)
    price: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str]
    location: Mapped[str]
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
    url: Mapped[str | None] = mapped_column(default='https://n1s1.hsmedia.ru/be/90/34/be9034d762857e5ba510937ce31b14b9/728x728_1_666010ab55120072825c74de5a7e19b0@1000x1000_0x10fmyjvQ_7882540427738188474.jpg.webp')
    order_index: Mapped[int]

    pet: Mapped['Pet'] = relationship('Pet', back_populates='photos')
    
