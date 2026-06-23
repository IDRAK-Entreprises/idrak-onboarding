from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)


class BottleStyle(Base):
    __tablename__ = "bottle_styles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    bottle = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    rope = Column(String, nullable=False)


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending", nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    worker = relationship("Worker")
    items = relationship("OrderItem")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    bottle_style_id = Column(Integer, ForeignKey("bottle_styles.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order")
    product = relationship("Product")
    bottle_style = relationship("BottleStyle")
