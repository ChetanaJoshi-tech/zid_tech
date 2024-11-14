# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, Sequence
from zid.database import Base
import datetime

class SalesProducts(Base):
    __tablename__ = 'sales__products'
     # Adjust schema if needed

    id = Column(Integer, Sequence("id"), primary_key=True)
    product_name = Column(String(64512))
    total_sales_value = Column(Float)
    orders_count = Column(Integer)
    product_sku = Column(String)
    created_at = Column(DateTime)
