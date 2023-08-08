import decimal
from pydantic import BaseModel, Field, EmailStr
from datetime import date

class User(BaseModel):
    id: int
    name: str = Field(..., title="Name", min_length=2)
    surname: str = Field(..., title="Surname", min_length=2)
    email: EmailStr = Field(..., title="Email", max_length=120)

class UserIn(BaseModel):
    name: str = Field(..., title="Name", min_length=2)
    surname: str = Field(..., title="Surname", min_length=2)
    email: EmailStr = Field(..., title="Email", max_length=120)
    password: str = Field(..., title="Password", min_length=9, max_length=25)

class Product(BaseModel):
    id: int
    product_name: str = Field(..., title="Product name")
    description: str = Field(..., title="Product description")
    price: int = Field(..., title="Price")

class ProductIn(BaseModel):
    product_name: str = Field(..., title="Product name")
    description: str = Field(..., title="Product description")
    price: int = Field(..., title="Price")

class Order(BaseModel):
    id: int
    user: User
    product: list[Product]
    date: date = Field(..., title="Date of order")
    is_delivered: bool = Field(..., title="Is delivered")

class OrderIn(BaseModel):
    user_id: int = Field(..., title="id of user")
    product_id: int = Field(..., title="id of product")
    date: date = Field(..., title="Date of order")
    is_delivered: bool = Field(..., title="Is delivered")

