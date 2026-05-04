from fastapi import FastAPI
from app.routes import products
from app.routes import orders
from app.routes import workers
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API working"}

app.include_router(orders.router)

app.include_router(products.router)

app.include_router(workers.router)