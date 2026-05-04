from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.products import Product
from app.models.bottle_styles import BottleStyle

router = APIRouter()

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    bottle_styles = db.query(BottleStyle).all()
    products = db.query(Product).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "bottle_styles": [{"id": bs.id, "name": bs.name, "bottle": bs.bottle, "cap": bs.cap, "rope": bs.rope} for bs in bottle_styles]
        })
    return result

@router.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    bottle_styles = db.query(BottleStyle).all()
    return {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "bottle_styles": [{"id": bs.id, "name": bs.name, "bottle": bs.bottle, "cap": bs.cap, "rope": bs.rope} for bs in bottle_styles]
    }