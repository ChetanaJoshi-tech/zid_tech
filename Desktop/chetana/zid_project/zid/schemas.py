# # app/schemas.py
# from pydantic import BaseModel
# from typing import Optional

# class SalesProductBase(BaseModel):
#     order_event_date: Optional[str]  # Use `str` here to allow any date format for input
#     store_id: Optional[int] = None
#     orders_year: Optional[float] = None
#     orders_quarter: Optional[float] = None
#     orders_month: Optional[float] = None
#     product_id: Optional[str] = None
#     product_name: Optional[str] = None
#     product_name_ar: Optional[str] = None
#     orders_count: Optional[int] = None
#     total_sales_value: Optional[float] = None
#     cogs: Optional[float] = None
#     net_revenue: Optional[float] = None
#     total_discounted_value: Optional[float] = None
#     shipping_revenue: Optional[float] = None
#     shipping_cost: Optional[float] = None
#     payment_processing_fees: Optional[float] = None
#     tax_amount: Optional[float] = None
#     delivered_orders_count: Optional[int] = None
#     delivered_orders_total_value_converted: Optional[float] = None
#     canceled_returned_orders_count: Optional[int] = None
#     canceled_returned_orders_total_value_converted: Optional[float] = None
#     last_updated_at_utc: Optional[str] = None
#     run_started_at_utc: Optional[str] = None
#     invocation_id: Optional[str] = None
#     product_sku: Optional[str] = None

# # For returning the created object
# class SalesProductOut(SalesProductBase):
#     id: int

#     class Config:
#         orm_mode = True  # This tells Pydantic to convert from SQLAlchemy model to dictionary


# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema to handle product creation
class SalesProductCreate(BaseModel):
    product_name: str
    total_sales_value: float
    orders_count: int
    product_sku: str
    created_at: Optional[datetime] = None  # Optional field for creation, default will be handled by DB

    class Config:
        orm_mode = True  # Tells Pydantic to treat ORM models (SQLAlchemy models) like dictionaries

# Schema to read a product (including the 'id' field)
class SalesProductRead(SalesProductCreate):
    id: int  # 'id' is added in the read schema, which will be returned by the DB
    
    class Config:
        orm_mode = True  # Allows Pydantic to read from ORM models
