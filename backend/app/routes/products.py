from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()

class CreateProduct(BaseModel):
    scent_name: str
    price: float


@router.get("/products")
def get_products():
    return {"products": []}

@router.get("/products/{id}")
def get_product_id(id:int):
    return {"products":id}


@router.post("/products")
def create_product(product: CreateProduct):
    return {
        "message":"Product created",
        "product": product
    }
