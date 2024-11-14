# # app/crud.py
# from sqlalchemy.orm import Session
# from zid.models import SalesProducts
# # from zid.schemas import SalesProductBase

# def create_sales_product(db: Session):
#     db_product = SalesProducts()  # Unpack Pydantic model
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# def get_sales_products(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(SalesProducts).offset(skip).limit(limit).all()


# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func
import datetime
import random

def create_sales_product(db: Session, sales_product: schemas.SalesProductCreate):
    db_product = models.SalesProducts(
        product_name=sales_product.product_name,
        total_sales_value=sales_product.total_sales_value,
        orders_count=sales_product.orders_count,
        product_sku=sales_product.product_sku,
        created_at=sales_product.created_at  # Default will be handled by the DB if not provided
    )
    db.add(db_product)
    db.commit()  # Commit to save the record
    db.refresh(db_product)  # Refresh to get the product id after committing
    return db_product

def get_sales_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SalesProducts).offset(skip).limit(limit).all()

def get_sales_product(db: Session, product_id: int):
    return db.query(models.SalesProducts).filter(models.SalesProducts.id == product_id).first()


def get_sales_products_by_date_range(db: Session, start_date: datetime.date, end_date: datetime.date):
    # Query for products created within a specific date range
    return db.query(models.SalesProducts).filter(models.SalesProducts.created_at.between(start_date, end_date)).all()

def get_sales_products_created_today(db: Session):
    today = datetime.date.today()  # Get today's date
    return db.query(models.SalesProducts).filter(models.SalesProducts.created_at == today).all()

def get_sales_products_created_this_month(db: Session):
    # Extract the current month from the 'created_at' field and filter by it
    current_month = func.extract('month', models.SalesProducts.created_at) == datetime.date.today().month
    return db.query(models.SalesProducts).filter(current_month).all()

def get_sales_products_created_last_week(db: Session):
    # Get the date 7 days ago
    seven_days_ago = datetime.date.today() - datetime.timedelta(days=7)
    return db.query(models.SalesProducts).filter(models.SalesProducts.created_at >= seven_days_ago).all()

# def get_totals_sales_values_by_date_range(db: Session, start_date: datetime.date, end_date: datetime.date):
#     # Query to sum the total_sales_value for records between start_date and end_date
#     total_sales_value = db.query(func.sum(models.SalesProducts.total_sales_value)).filter(
#         models.SalesProducts.created_at.between(start_date, end_date)
#     ).scalar()  # .scalar() returns the result of the aggregate function (sum) directly

#     return total_sales_value


# def get_totals_sales_count_by_date_range(db: Session, start_date: datetime.date, end_date: datetime.date):
#     # Query to sum the total_sales_value for records between start_date and end_date
#     total_sales_count = db.query(func.count(models.SalesProducts.total_sales_value)).filter(
#         models.SalesProducts.created_at.between(start_date, end_date)
#     ).scalar()  # .scalar() returns the result of the aggregate function (sum) directly

#     return total_sales_count



def get_total_sales_count_and_avg_by_date_range(db: Session, start_date: datetime.date, end_date: datetime.date):
    # Query to sum the total_sales_value and count records between start_date and end_date
    result = db.query(
        func.sum(models.SalesProducts.total_sales_value).label('total_sales_value'),
        func.count(models.SalesProducts.id).label('total_count'),
        func.avg(models.SalesProducts.total_sales_value).label('tatal_sales_avg')
    ).filter(
        models.SalesProducts.created_at.between(start_date, end_date)
    ).first()  # Use .first() to get the first (and only) result
    
    # If no result is found, return (None, None) instead of None
    if result is None:
        return (None, None)
    
    return result