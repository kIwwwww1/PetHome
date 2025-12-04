from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    role: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

class Pet(Base):
    __tablename__ = 'pets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    breed: Mapped[str]
    description: Mapped[str]
    location: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    owner_id: Mapped[int]

class PetPhoto(Base):
    __tablename__ = 'pet_photos'

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int]
    url: Mapped[str]
    order_index: Mapped[int]

    
