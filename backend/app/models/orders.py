from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False, default = "pending")
    customer_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    #so everyime an order is completed we want to know who completed it. This forigen key
    #connected to the worker id, allows us to track who completed what.
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    items = relationship("OrderItem", back_populates="order")