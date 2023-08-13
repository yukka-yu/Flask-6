import sqlalchemy
from sqlalchemy import create_engine
import databases
from settings import settings
from sqlalchemy.schema import ForeignKey
#from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey('users.id'),
		nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, ForeignKey('products.id'), nullable=False),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("is_delivered", sqlalchemy.Boolean),

    #user = relationship("User", back_populates="orders"),
    #product = relationship("Product", back_populates="orders"),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)