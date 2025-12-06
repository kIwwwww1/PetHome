from typing import Literal
from pydantic import BaseModel, Field, EmailStr

Roles = Literal['salesman','buyer', 'admin']

class UserData(BaseModel):
    password: str = Field(min_length=8, max_length=15)
    email: EmailStr


class NewUser(UserData):
    name: str = Field(min_length=3, max_length=15)
    role: Roles
