#implement tables
from pydantic_core.core_schema import nullable_schema
from sqlalchemy import Column,String,DateTime,Boolean, false, null,ForeignKey,Integer,Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key = True, default = uuid.uuid4(), index = True)
    email = Column(String(100),unique = True, nullable = False,index = True)
    first_name = Column(String(100), nullable = False),
    last_name = Column(String(100), nullable = False)
    country = Column(String(100),nullable = False)
    city = Column(String(100),nullable = False)
    zip_code = Column(String(100),nullable = False)
    shipping_address_1 = Column(String(100),nullable = False)
    shipping_address_2 = Column(String(100),nullable = True)
    created_at = Column(DateTime,nullable=False,default=datetime.datetime.now(datetime.timezone.utc))

class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(UUID(as_uuid = True),primary_key = True, index = True,default = uuid.uuid4(),index = True )
    product_id = Column(UUID(as_uuid = True),ForeignKey('products.id',ondelete='CASCADE'),nullable = False,index=True)
    user_id = Column(UUID(as_uuid = True),ForeignKey('users.id', ondelete='CASCADE'), nullable = False,index=True)
    quantity = Column(Integer,nullable=False)
    #relationships
    user = relationship("User",back_populates='cart_items')
    product = relationship("Product",back_populates='cart_items')

class Products(Base):

    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True),primary_key = True,default = uuid.uuid4(),index = True)
    product_name = Column(String(100),nullable = False)
    description = Column(String(100),nullable = False)
    price = Column(Float,nullable = False)
    created_at = Column(DateTime,nullable=False,default=datetime.datetime.now(datetime.timezone.utc))
    update_at = Column(DateTime,nullable=False,default=datetime.datetime.now(datetime.timezone.utc))
