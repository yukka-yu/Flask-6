from fastapi import APIRouter, HTTPException
from db import users, products, orders, database
from models import User, UserIn, Product, ProductIn, Order, OrderIn
from bcrypt import gensalt, hashpw

router = APIRouter()

# USER ROUTES

@router.get("/users", response_model=list[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@router.post("/users", response_model=User)
async def create_user(user: UserIn):
    #Хэшируем пароль
    salt = gensalt()
    password_hash = hashpw(user.password.encode("utf-8"), salt)
    user.password = password_hash
    #
    query = users.insert().values(**user.model_dump())
    last_id = await database.execute(query)
    return {**user.model_dump(), "id":last_id}

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    res = await database.fetch_one(query)
    if not res:
        raise HTTPException(status_code=404, detail='User not found')
    return res


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id ==
                                 user_id).values(**new_user.model_dump())
    data = await database.execute(query)
    if data > 0:
        return {**new_user.model_dump(), "id": user_id}
    raise HTTPException(status_code=404, detail='User not found')


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}



# PRODUCT ROUTES

@router.get("/products", response_model=list[Product]) 
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


@router.post("/products", response_model=Product)
async def create_product(product: ProductIn):
    #
    query = products.insert().values(**product.model_dump())
    last_id = await database.execute(query)
    return {**product.model_dump(), "id":last_id}

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    res = await database.fetch_one(query)
    if not res:
        raise HTTPException(status_code=404, detail='product not found')
    return res


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id ==
                                 product_id).values(**new_product.model_dump())
    data = await database.execute(query)
    if data > 0:
        return {**new_product.model_dump(), "id": product_id}
    raise HTTPException(status_code=404, detail='product not found')


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    data = await database.execute(query)
    if data > 0: 
        return {'message': 'product deleted'}
    raise HTTPException(status_code=404, detail='product not found')


# ORDER ROUTES
 
# Хотим вывести все заказы:
@router.get("/orders", response_model=list[Order]) 
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)

