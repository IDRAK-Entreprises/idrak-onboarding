from app.database import SessionLocal
from app.models.products import Product
from app.models.bottle_styles import BottleStyle

def seed():
    db = SessionLocal()

    bottle_styles = [
        {"name": "Blacktop", "bottle": "Clear glass", "cap": "Black plastic", "rope": "Black"},
        {"name": "Classic", "bottle": "Clear glass", "cap": "Wooden", "rope": "Gold/tan"},
        {"name": "Smoky Black", "bottle": "Dark tinted glass", "cap": "Black plastic", "rope": "Black"},
        {"name": "Frosted Black", "bottle": "Frosted glass", "cap": "Black plastic", "rope": "Black"},
        {"name": "Frosted Wood", "bottle": "Frosted glass", "cap": "Wooden", "rope": "Gold/tan"},
        {"name": "Smoky Wood", "bottle": "Dark tinted glass", "cap": "Wooden", "rope": "Gold/tan"},
    ]

    products = [
        {"name": "Berry Elixir", "price": 18.49},
        {"name": "Burnout", "price": 17.99},
        {"name": "Carbon Ice", "price": 17.99},
        {"name": "Crystal Breeze", "price": 19.99},
        {"name": "Formula Bleu", "price": 19.99},
        {"name": "Formula Creed", "price": 17.99},
        {"name": "Formula Intensely", "price": 17.99},
        {"name": "Formula Layton", "price": 17.99},
        {"name": "Formula Savage", "price": 17.99},
        {"name": "Garden of Eden", "price": 17.99},
        {"name": "Liquid Gold", "price": 17.99},
        {"name": "Mornin' Wood", "price": 17.99},
        {"name": "Pure Adrenaline", "price": 17.99},
        {"name": "Redline", "price": 17.99},
        {"name": "Titanium", "price": 17.99},
    ]

    for bs in bottle_styles:
        db.add(BottleStyle(**bs))

    for p in products:
        db.add(Product(**p))

    db.commit()
    db.close()
    print("Database seeded")

if __name__ == "__main__":
    seed()