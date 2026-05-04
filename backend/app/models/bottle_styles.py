from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class BottleStyle(Base):
    __tablename__ = "bottle_styles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bottle = Column(String, nullable=False)
    cap = Column(String, nullable=False)
    rope = Column(String, nullable=False)
    order_items = relationship("OrderItem", back_populates="bottle_style")