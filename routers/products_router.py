import os
import sys

from sqlalchemy import exc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas import Product
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Products
from schemas import Product,ProductUpdate
import uuid

products_app = APIRouter(
    title = "Products Router"
)

products_app.get("/products",response_model=List[Product])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Get all products 
    """
    try:
        products = db.query(Products).all()
        return [Product.model_validate(product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500,detail = f"Database Error:{e}")

products_app.get("/products/{id}",reponse_model =List[Product])
async def get_product_by_id(id:str,db: Session = Depends(get_db)):
    """
    get a product by id
    """
    try:
        products = db.query(Products).filter(Products.id == id)
        return [Product.model_validate(product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500,detail = f"DB Error getting product by id {e}")

products_app.put("/products/{id}",response_model = Product)
async def update_product_by_id(product_updates:ProductUpdate, db:Session = Depends(get_db)):
        """
        Update a product by ID
        """
        try:
            try:
                product_uuid = uuid.UUID(id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid product ID format")
            
            # Get product from database
            selected_product = db.query(Products).filter(Products.id == product_uuid).first()
            if not selected_product:
                raise HTTPException(status_code=404, detail=f'Product with id {id} not found')
            
            # Get only provided fields
            updates_dict = product_updates.model_dump(exclude_unset=True)
            
            # Updates
            for field, update in updates_dict.items():
                setattr(selected_product, field, update)
            
            # Save to database
            db.commit()
            db.refresh(selected_product)
            
            # Return updated product
            return Product.model_validate(selected_product)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update product: {e}")


