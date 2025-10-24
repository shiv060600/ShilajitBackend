from itertools import product
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
    @model_validator(mode = 'after')
    def validate_user_create(self):
        if '@' not in self.email:
            raise ValueError('Invalid Email format')

        required_fields = [
            self.email,self.first_name,
            self.last_name,self.country,
            self.city,self.state,
            self.zip_code,self.shipping_address_1
        ]

        if not all(required_fields):
            raise ValidationError("One or more user_create fields is missing")
        
        if not all([field != '' for field in required_fields]):
            raise ValidationError("One or more fields is an empty string")

class UserUpdate(BaseModel):
    id:str
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
        except ValueError as ve:
            print(f"value error: {ve}")
        required_fields = [self.email,self.first_name,self.last_name,
                        self.country,self.city,self.state,self.zip_code,
                        self.shipping_address_1]

        if not all(required_fields):
            raise ValidationError("one or more of required fields is missing")
        
        if not all([field != '' for field in required_fields]):
            raise ValidationError("one or more fields is an empty string")

        return self

class UserDelete(BaseModel):
    id:str
    @model_validator(mode = 'after')
    def validate_user_delete(self):
    
        try:
            uuid.UUID(self.id)
        except ValueError as ve:
            print(f"value error deleting user {ve}")
            raise ValidationError("invalid user_id")

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
        if self.quantity < 0:
            raise ValidationError("quanitity can be less than 0")
        if not self.quantity:
            raise ValidationError("Quanitity cannot be null")

        try:
            uuid.UUID(self.id)
        except ValueError as ve:
            print(f"Value error when updating validate: {ve}")
            raise ValidationError("Failed to validate user id")
        return self

class DeleteCartItem(BaseModel):
    id:str
    @model_validator(mode='after')
    def validate_delete_cart_item(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ve:
            print(f"invalid uuid: {ve}")
            raise ValidationError("Failed to validate user id")
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
            raise ValidationError("length of products does not match length of quantities")
        
        if not all(qty != 0 for qty in self.product_quantities):
            raise ValidationError("cannot order quantity zero")
        
        
        for id in self.product_ids:
            try:
                uuid.UUID(id)
            except ValueError as ve:
                print(f"product id is not a valid UUID")
                raise ValidationError("Product ID is not a valid uuid")

        return self

        
        


