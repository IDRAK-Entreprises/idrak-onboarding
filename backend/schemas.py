from pydantic import BaseModel
from typing import List, Optional

class OrderItemCreate(BaseModel):
    product_id: int
    bottle_style_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class WorkerCreate(BaseModel):
    name: str

class FulfillRequest(BaseModel):
    worker_id: int
