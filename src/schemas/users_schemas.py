import re
from typing import Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

Roles = Literal['salesman','buyer', 'admin']

class UserData(BaseModel):
    password: str = Field(min_length=8, max_length=15)
    email: EmailStr


class NewUser(UserData):
    name: str = Field(min_length=3, max_length=15)
    role: Roles

class ContactPhone(BaseModel):
    phone: str

    @field_validator("phone")
    def validate_russian_phone(cls, phone):
        if not re.fullmatch(r'^\+?[1-9]\d{7,14}$', phone):
            raise ValueError("Некорректный формат номера телефона")
        
        if not phone.startswith("+7"):
            raise ValueError("Должен быть российский номер, начинающийся с +7")
        
        return phone


class ContactTelegram(BaseModel):
    telegram: str
    
    @field_validator("telegram")
    def validate_telegram(cls, telegram):
        if not re.fullmatch(r"^@[a-zA-Z0-9_]{5,32}$", telegram):
            raise ValueError(
                "Некорректный username Telegram. Используйте @username"
            )
        return telegram
