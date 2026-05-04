from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orders import Order
from app.models.order_items import OrderItem
from typing import List
from pydantic import BaseModel

router = APIRouter()

class OrderItemInput(BaseModel):
    product_id: int
    bottle_style_id: int
    quantity: int

class OrderInput(BaseModel):
    customer_name: str
    items: List[OrderItemInput]

@router.post("/orders")
def create_order(order: OrderInput, db: Session = Depends(get_db)):
    db_order = Order(customer_name=order.customer_name, status="pending")
    db.add(db_order)
    db.flush()
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            bottle_style_id=item.bottle_style_id,
            quantity=item.quantity
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/queue")
def get_queue(db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.status == "pending").order_by(Order.created_at.asc()).first()
    if not order:
        raise HTTPException(status_code=404, detail="No pending orders")
    return order

@router.get("/orders")
def get_orders(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    return query.all()

@router.get("/orders/{id}")
def get_order(id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "created_at": order.created_at,
        "worker_id": order.worker_id,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "bottle_style_id": item.bottle_style_id,
                "quantity": item.quantity
            } for item in order.items
        ]
    }

@router.post("/orders/{id}/fulfill")
def fulfill_order(id: int, worker_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == "completed":
        raise HTTPException(status_code=400, detail="Order already fulfilled")
    order.status = "completed"
    order.worker_id = worker_id
    db.commit()
    db.refresh(order)
    return order    