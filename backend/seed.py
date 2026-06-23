from decimal import Decimal
from database import SessionLocal
from models import Product, BottleStyle, Worker

products = [
    ("Berry Elixir", Decimal("18.49")),
    ("Burnout", Decimal("17.99")),
    ("Carbon Ice", Decimal("17.99")),
    ("Crystal Breeze", Decimal("19.99")),
    ("Formula Bleu", Decimal("19.99")),
    ("Formula Creed", Decimal("17.99")),
    ("Formula Intensely", Decimal("17.99")),
    ("Formula Layton", Decimal("17.99")),
    ("Formula Savage", Decimal("17.99")),
    ("Garden of Eden", Decimal("17.99")),
    ("Liquid Gold", Decimal("17.99")),
    ("Mornin' Wood", Decimal("17.99")),
    ("Pure Adrenaline", Decimal("17.99")),
    ("Redline", Decimal("17.99")),
    ("Titanium", Decimal("17.99")),
]

bottle_styles = [
    ("Blacktop", "Clear glass", "Black plastic", "Black"),
    ("Classic", "Clear glass", "Wooden", "Gold/tan"),
    ("Smoky Black", "Dark tinted glass", "Black plastic", "Black"),
    ("Frosted Black", "Frosted glass", "Black plastic", "Black"),
    ("Frosted Wood", "Frosted glass", "Wooden", "Gold/tan"),
    ("Smoky Wood", "Dark tinted glass", "Wooden", "Gold/tan"),
]

db = SessionLocal()

for name, price in products:
    product = Product(name=name, price=price)
    db.add(product)

for name, bottle, cap, rope in bottle_styles:
    style = BottleStyle(name=name, bottle=bottle, cap=cap, rope=rope)
    db.add(style)

worker1 = Worker(name="Alex")
worker2 = Worker(name="Sam")

db.add(worker1)
db.add(worker2)

db.commit()
db.close()

print("Seed data added")
