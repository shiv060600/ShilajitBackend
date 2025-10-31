from itertools import product
from optparse import Option
from pydantic import BaseModel,field_validator,model_validator,ValidationError
from typing import Optional
import datetime
import uuid

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
    shipping_address_2: Optional[str]
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
    shipping_address_2: Optional[str]
    
    @model_validator(mode='after')
    def validate_user_create(self):
        if '@' not in self.email:
            raise ValueError('Invalid Email format')

        required_fields = [
            self.email, self.first_name,
            self.last_name, self.country,
            self.city, self.state,
            self.zip_code, self.shipping_address_1
        ]

        if not all(required_fields):
            raise ValueError("One or more user_create fields is missing")
        
        if not all([field != '' for field in required_fields]):
            raise ValueError("One or more fields is an empty string")
        
        return self

class UserUpdate(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    country: str
    city: str
    state: str
    zip_code: str
    shipping_address_1: str
    shipping_address_2: Optional[str]
    
    @model_validator(mode='after')
    def validate_user(self):
        try:
            uuid.UUID(self.id)
        except ValueError:
            raise ValueError("Invalid user_id UUID format")
        
        required_fields = [
            self.email, self.first_name, self.last_name,
            self.country, self.city, self.state, self.zip_code,
            self.shipping_address_1
        ]

        if not all(required_fields):
            raise ValueError("One or more of required fields is missing")
        
        if not all([field != '' for field in required_fields]):
            raise ValueError("One or more fields is an empty string")

        return self

class UserDelete(BaseModel):
    id: str
    
    @model_validator(mode='after')
    def validate_user_delete(self):
        try:
            uuid.UUID(self.id)
        except ValueError:
            raise ValueError("Invalid user_id UUID format")
        
        return self

class UserReponse(BaseModel):
    email: str
    first_name: str
    last_name: str
    country: str
    city: str
    state: str
    zip_code: str
    shipping_address_1: str
    shipping_address_2: Optional[str]

class CartItem(BaseModel):
    id: str
    user_id: str
    product_id: str
    product_name:str
    quantity: int

class UpdateCartItem(BaseModel):
    id: str
    quantity: int

    @model_validator(mode='after')
    def validate_update_cart_item(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        try:
            uuid.UUID(self.id)
        except ValueError:
            raise ValueError("Invalid cart item ID UUID format")
        
        return self

class DeleteCartItem(BaseModel):
    id: str
    
    @model_validator(mode='after')
    def validate_delete_cart_item(self):
        try:
            uuid.UUID(self.id)
        except ValueError:
            raise ValueError("Invalid cart item ID UUID format")
        
        return self

class CartItemResponse(BaseModel):
    user_id: str
    product_id: str
    product_name: str
    quantity: int

class Order(BaseModel):
    id: str
    user_id: str
    product_ids: list[str]
    product_quantities: list[int]


class CreateOrder(BaseModel):
    user_id: str
    product_ids: list[str]
    product_quantities: list[int]
    
    @model_validator(mode='after')
    def validate_create_order(self):
        if len(self.product_ids) != len(self.product_quantities):
            raise ValueError("Length of products does not match length of quantities")
        
        if not all(qty > 0 for qty in self.product_quantities):
            raise ValueError("All quantities must be greater than zero")
        
        for product_id in self.product_ids:
            try:
                uuid.UUID(product_id)
            except ValueError:
                raise ValueError(f"Product ID '{product_id}' is not a valid UUID")
        
        return self

class DeleteOrder(BaseModel):
    id: str
    
    @model_validator(mode='after')
    def validate_delete_order(self):
        if not self.id:
            raise ValueError("Order ID is required")
        
        try:
            uuid.UUID(self.id)
        except ValueError:
            raise ValueError("Invalid order ID UUID format")
        
        return self

class Product(BaseModel):
    id: str
    description: str
    price: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str

class ProductUpdate(BaseModel):
    description: Optional[str] = None
    price: Optional[float] = None
    product_name: Optional[str] = None
    
    @model_validator(mode='after')
    def validate_update_model(self):
        if self.price is not None and self.price <= 0:
            raise ValueError("Price must be greater than 0")
        
        if self.product_name is not None and not self.product_name.strip():
            raise ValueError("Product name cannot be empty")
        
        return self  




    



        
        


