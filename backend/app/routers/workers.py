from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.workers import Worker
from app.models.orders import Order
from pydantic import BaseModel

router = APIRouter()

class WorkerInput(BaseModel):
    name: str

@router.post("/workers")
def create_worker(worker: WorkerInput, db: Session = Depends(get_db)):
    db_worker = Worker(name=worker.name)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.get("/workers/{id}/stats")
def get_worker_stats(id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    total = db.query(Order).filter(Order.worker_id == id).count()
    return {"worker_id": id, "name": worker.name, "orders_fulfilled": total}