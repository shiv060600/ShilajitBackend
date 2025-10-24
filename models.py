#implement tables
from sqlalchemy import Column,String,DateTime,Boolean, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key = True, default = uuid.uuid4, index = True)
    email = Column(String(100),unique = True, nullable = False,index = True)
    first_name = Column(String(100), nullable = False),
    last_name = Column(String(100), nullable = False)
    country = Column(String(100),nullable = False)