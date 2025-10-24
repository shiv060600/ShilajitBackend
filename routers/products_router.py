import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas import Product
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Products
from schemas import Product

products_app = APIRouter(
    title = "Products Router"
)

products_app.get("/products",response_model=List[Product])
async def get_all_products(
    db: Session = Depends(get_db)
    ):
    """
    Get all products 
    """
    try:
        products = db.query(Product).all()
        return [Product.model_validate(product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500,detail = f"Database Error:{e}")


