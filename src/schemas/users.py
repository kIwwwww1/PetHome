from typing import Literal
from pydantic import BaseModel, Field, EmailStr

Roles = Literal['salesman','buyer', 'admin']

class User(BaseModel):
    name: str = Field(min_length=3, max_length=15)
    email: EmailStr
    role: Roles