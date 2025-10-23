from pydantic import BaseModel
from typing import Optional
import datetime

class User(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    country: str
    city: str
    state: str
    zip_code: str
    shipping_address_1: str
    shipping_address_2: str
    created_at: datetime.datetime

class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    country: str
    city: str
    state: str
    zip_code: str
    shipping_address_1: str
    shipping_address_2: str