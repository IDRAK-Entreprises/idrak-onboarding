from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import Product, BottleStyle, Worker, Order, OrderItem
from schemas import OrderCreate, WorkerCreate, FulfillRequest

app = FastAPI(title="IDRAK Order Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def make_order_result(order):
    items = []

    for item in order.items:
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "bottle_style_id": item.bottle_style_id,
            "bottle_style_name": item.bottle_style.name,
            "quantity": item.quantity
        })

    return {
        "id": order.id,
        "status": order.status,
        "worker_id": order.worker_id,
        "created_at": order.created_at,
        "completed_at": order.completed_at,
        "items": items
    }

@app.get("/")
def home():
    return {"message": "IDRAK backend is running"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.id).all()
    bottle_styles = db.query(BottleStyle).order_by(BottleStyle.id).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "bottle_styles": bottle_styles
        })

    return result

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    bottle_styles = db.query(BottleStyle).order_by(BottleStyle.id).all()

    return {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "bottle_styles": bottle_styles
    }

@app.post("/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    if len(order_data.items) == 0:
        raise HTTPException(status_code=400, detail="Order needs at least one item")

    new_order = Order(status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        bottle_style = db.query(BottleStyle).filter(BottleStyle.id == item.bottle_style_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        if bottle_style is None:
            raise HTTPException(status_code=404, detail="Bottle style not found")

        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            bottle_style_id=item.bottle_style_id,
            quantity=item.quantity
        )

        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return make_order_result(new_order)

@app.get("/orders")
def get_orders(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Order)

    if status is not None:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.id).all()
    return [make_order_result(order) for order in orders]

@app.get("/orders/queue")
def get_queue(db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .filter(Order.status != "completed")
        .order_by(Order.id)
        .first()
    )

    if order is None:
        raise HTTPException(status_code=404, detail="No orders in queue")

    return make_order_result(order)

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return make_order_result(order)

@app.post("/orders/{order_id}/fulfill")
def fulfill_order(order_id: int, data: FulfillRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    worker = db.query(Worker).filter(Worker.id == data.worker_id).first()

    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    if order.status == "completed":
        raise HTTPException(status_code=400, detail="Order already completed")

    order.status = "completed"
    order.worker_id = worker.id
    order.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(order)

    return make_order_result(order)

@app.post("/workers")
def create_worker(worker_data: WorkerCreate, db: Session = Depends(get_db)):
    worker = Worker(name=worker_data.name)
    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker

@app.get("/workers/{worker_id}/stats")
def get_worker_stats(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    total = db.query(Order).filter(
        Order.worker_id == worker.id,
        Order.status == "completed"
    ).count()

    return {
        "worker_id": worker.id,
        "worker_name": worker.name,
        "total_orders_fulfilled": total
    }
