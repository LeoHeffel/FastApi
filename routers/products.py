from fastapi import APIRouter, HTTPException
#from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"], responses={404: {"description": "Not found"}})

@router.get("/")
async def get_products():
    return [{"id": 1, "name": "Product 1"}, {"id": 2, "name": "Product 2"}]

@router.get("/{product_id}")
async def get_products_by_id(product_id: int):
    return [{"id": product_id, "name": f"Product {product_id}"}]