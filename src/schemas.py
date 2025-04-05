from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MenuItem(BaseModel):
    id: int
    dish_name: str
    image: Optional[str]
    is_available: bool
    description: Optional[str]

    class Config:
        orm_mode = True

class MenuItemCreate(BaseModel):
    dish_name: str
    image: Optional[str]
    is_available: bool = True
    description: Optional[str]