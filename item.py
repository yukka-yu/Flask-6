from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from db import users, products, orders, database
from models import OrderIn, User, UserIn, Product, ProductIn, Order
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
    query = (
        select(
            orders.c.id,
            users.c.id.label("user_id"),
            users.c.name,
            users.c.surname,
            users.c.email,
            products.c.id.label("product_id"),
            products.c.product_name,
            products.c.description,
            products.c.price,
        )
        .join(users)
        .join(products)
    )
    print(query)
    res = await database.fetch_all(query)
    return [
        Order(
            id=r.id,
            user=User(
                id=r.user_id,
                name=r.name,
                surname=r.surname,
                email=r.email
            ),
            product=Product(
                id=r.product_id,
                product_name=r.product_name,
                description=r.description,
                price=r.price
    )
        ) for r in res]

# # TEST
# @router.get("/test")
# async def get_test():
#     query = (
#         select(
#             orders.c.id,
#             users.c.id.label("user_id"),
#             users.c.name,
#             users.c.surname,
#             users.c.email,
#             products.c.id.label("product_id"),
#             products.c.product_name,
#             products.c.description,
#             products.c.price,
#         )
#         .join(users)
        
#     )
#     print(query)

# Добавляем заказ   
@router.post("/orders", response_model=Order)
async def create_order(new_order: OrderIn):
    query = orders.insert().values(**new_order.model_dump())
    last_id = await database.execute(query)
    return {**new_order.model_dump(), "id":last_id}

# Выводим заказ по номеру
@router.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = select(
        orders.c.id,
        users.c.id.label("user_id"),
        users.c.name,
        users.c.surname,
        users.c.email,
        products.c.id.label("product_id"),
        products.c.product_name,
        products.c.description,
        products.c.price,
        ).where(orders.c.id == order_id).join(users).join(products)
        
        
    r = await database.fetch_one(query)
    if not r:
        raise HTTPException(status_code=404, detail='order not found')
    return Order(
            id=r.id,
            user=User(
                id=r.user_id,
                name=r.name,
                surname=r.surname,
                email=r.email
                ),
            product=Product(
                id=r.product_id,
                product_name=r.product_name,
                description=r.description,
                price=r.price
                )
            )
# Вносим изменения в заказ. Здесь бы можно было обработать многочисленные ошибки: пользователь с таким id не найден и т.д., но нет сил
@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id ==
                                 order_id).values(**new_order.model_dump())
    query_user = users.select().where(users.c.id == new_order.user_id)
    query_product = products.select().where(products.c.id == new_order.product_id)
    data = await database.execute(query)
    res_user = await database.fetch_one(query_user)
    res_product = await database.fetch_one(query_product)
    if data > 0:
        # return Order(
        #         id=order_id,
        #         user=res_user,
        #         product=res_product
        #         )
        return {"id":order_id, "user":res_user, "product":res_product, "date":new_order.date, "is_delivered":new_order.is_delivered}
    raise HTTPException(status_code=404, detail='order not found')

@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    data = await database.execute(query)
    if data > 0: 
        return {'message': 'order deleted'}
    raise HTTPException(status_code=404, detail='order not found')
