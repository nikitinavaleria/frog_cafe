from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    category: Optional[str]
    quantity_left: int

    class Config:
        from_attributes = True

class MenuItemCreate(BaseModel):
    dish_name: str
    image: Optional[str] = None
    is_available: bool = True
    description: Optional[str] = None
    category: Optional[str] = None
    quantity_left: int = 10

class MenuItemUpdate(BaseModel):
    dish_name: Optional[str]
    image: Optional[str]
    is_available: Optional[bool]
    description: Optional[str]
    category: Optional[str]
    quantity_left: Optional[int]



class User(BaseModel):
    id: int
    name: str
    role_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    password: str
    role_id: int


class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str


class OrderStatus(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class OrderStatusCreate(BaseModel):
    name: str


class Toad(BaseModel):
    id: int
    pic: str
    is_taken: bool

    class Config:
        from_attributes = True

class ToadCreate(BaseModel):
    pic: str
    is_taken: bool = False

class Order(BaseModel):
    id: int
    user_id: int
    toad_id: int
    status_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int  # мы будем получать из токена, но пусть пока будет
    # корзина пока пропускаем, можно добавить позже

class OrderStatusUpdate(BaseModel):
    status_id: int

class CartItem(BaseModel):
    id: int
    dish_name: str
    image: Optional[str]
    description: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True


class TVOrder(BaseModel):
    id: int
    user_id: int
    toad_id: int
    status_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class CartAddMultiple(BaseModel):
    menu_items: list[int]
