from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, orders, workers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(workers.router)

@app.get("/")
def root():
    return {"message": "IDRAK Order Management API"}