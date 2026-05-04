from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
class CreateWorker(BaseModel):
    name: str

@router.get("/workers/{id}/stats")
def get_worker_stats(id: int):
    return {"worker_id": id, "orders_completed": 0}

@router.post("/workers")
def create_worker(worker: CreateWorker):
    return {
        "message": "Worker created",
        "worker": worker
    }