from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()
class CreateOrderItem(BaseModel):
    product_id: int
    bottle_style_id :int
    quantity:int

class CreateOrder(BaseModel):
    items: List[CreateOrderItem]

@router.get("/orders")
def get_orders():
    return {"orders" : []}

@router.get("/orders/{id}")
def get_orders_id(id: int):
    return {"orders" :id}

@router.get("/orders/queue")
def get_orders_queue():
    return {"orders" : []}

@router.post("/orders")
def create_order(order:CreateOrder):
    return {
        "message":"Order created",
        "order": order
    }

@router.post("/orders/{id}/fulfill")
def fulfill_order(id : int):
    return {
        "message": "Order fulfilled",
        "order_id" : id
    }